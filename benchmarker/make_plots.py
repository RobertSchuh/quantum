import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os

from quantum_tester import TesterGroup, test_on_random_circuits

if not "/usr/local/texlive/2023/bin/x86_64-linux" in os.environ["PATH"]:
    os.environ["PATH"] = "/usr/local/texlive/2023/bin/x86_64-linux" + os.pathsep + os.environ["PATH"]

# Initialize TesterGroup and define backends
tg = TesterGroup()
backends = ["ibm_perth", "ibmq_quito", "ibmq_lima", "qb-qdk1", "qb-nm2", "qb-nm1"]

# Define parameters
nc, shots = 50, 2000



def set_size(width, fraction=1):
    fig_width_pt = width * fraction
    inches_per_pt = 1 / 72.27
    golden_ratio = (5 ** .5 - 1) / 2
    fig_width_in = fig_width_pt * inches_per_pt
    fig_height_in = fig_width_in * golden_ratio
    fig_dim = (fig_width_in, fig_height_in)
    return fig_dim


# plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}, \usepackage{amsmath}"]
# Options
params = {'text.usetex': True,
          'font.size': 26,
          # 'font.family': 'aess17',
          }
plt.rcParams.update(params)
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')



# Create a function to plot the results
def plot_results(ngs, nqs, results, naive, title_suffix, plot_over_gates, filename_suffix, ax2):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)

    if plot_over_gates:
        x = ngs
        ax.set_xlabel("Number of gates")
        ax2.set_xlabel("Number of gates")
    else:
        x = nqs
        ax.set_xlabel("Number of qubits")
        ax2.set_xlabel("Number of qubits")
    for backend in backends:
        partial_res = np.array([result[backend] for result in results])
        ax.errorbar(
            x, np.mean(partial_res, axis=1), yerr=np.std(partial_res, axis=1),
            label=backend, marker="x", capsize=10, markersize=10
        )
        ax2.errorbar(
            x, np.mean(partial_res, axis=1), yerr=np.std(partial_res, axis=1),
            label=backend, marker="x", capsize=10, markersize=10
        )
    ax.grid()
    ax.legend()
    ax.set_ylabel("Error Score")
    ax2.grid()
    ax2.legend(fontsize=12)
    ax2.set_ylabel("Error Score")
    if naive:
        ax.set_title("Naive - " + title_suffix)
    else:
        ax.set_title("New attempt - " + title_suffix)
    ax2.set_title(title_suffix)

    filename = f"plots/error_plot_{filename_suffix}.png"
    fig.savefig(filename)
    # plt.show(block=False)
    plt.close(fig)



fig, axes = plt.subplots(2, 2, figsize=set_size(1075, fraction=1))
fig.subplots_adjust(hspace=0.45, wspace=0.3, top=0.95, bottom=0.1, left=0.1, right=0.98)
# fig.suptitle("Second attempt")
fign, axesn = plt.subplots(2, 2, figsize=set_size(1075, fraction=1))
fign.subplots_adjust(hspace=0.45, wspace=0.3, top=0.95, bottom=0.1, left=0.1, right=0.98)
# fign.suptitle("Naive approach")

# Define test cases and plot the results
test_cases = [
    (25 * np.arange(11), 2 + 0 * np.arange(11), True, "2 qubits", True, axesn[0][0]),
    (25 * np.arange(11), 2 + 0 * np.arange(11), False, "2 qubits", True, axes[0][0]),
    (10 * np.arange(11), 5 + 0 * np.arange(11), True, "5 qubits", True, axesn[1][0]),
    (10 * np.arange(11), 5 + 0 * np.arange(11), False, "5 qubits", True, axes[1][0]),
    (0 + 5 * (np.arange(10) + 1), np.arange(10) + 1, True, "5 gates per qubit", False, axesn[0][1]),
    (0 + 5 * (np.arange(10) + 1), np.arange(10) + 1, False, "5 gates per qubit", False, axes[0][1]),
    (25 + 0 * np.arange(10), np.arange(10) + 1, True, "25 gates total", False, axesn[1][1]),
    (25 + 0 * np.arange(10), np.arange(10) + 1, False, "25 gates total", False, axes[1][1])
]

# Calculate the total number of iterations
total_iterations = sum(len(ngs) for ngs, _, _, _, _, _ in test_cases)

# Initialize a single progress bar for the entire process
progress_bar = tqdm(total=total_iterations, desc="Overall Progress")

for ngs, nqs, naive, title_suffix, plot_over_gates, ax in test_cases:
    results = []

    for nq, ng in zip(nqs, ngs):
        # result = {backend: np.random.random(5) for backend in backends}
        result = test_on_random_circuits(tg, backends, nq=nq, ng=ng, nc=nc, shots=shots, naive=naive)
        results.append(result)
        progress_bar.update(1)

    plot_results(ngs, nqs, results, naive, title_suffix, plot_over_gates,
                 f"{title_suffix.replace(' ', '_').lower() + '_naive' * naive}", ax)

progress_bar.close()

fig.savefig("plots/new_attempt.pdf")
fign.savefig("plots/naive.pdf")
