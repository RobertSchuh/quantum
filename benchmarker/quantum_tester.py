import numpy as np
from qiskit import QuantumCircuit, Aer, transpile
from qiskit.circuit.random import random_circuit

from qiskit.providers.aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_provider import IBMProvider

# IBM quantum channel
QiskitRuntimeService.save_account(channel="ibm_quantum",
                                  token="75957d48e7acd59dee864e3c92f75b7b6befafd37e6f43b703f40fbfeed1cdb2406e6810336a13ad1d393009cd1f249cb3ebb222510676d94740aa1b85ee95a6",
                                  overwrite=True)

service = QiskitRuntimeService(channel="ibm_quantum")
ibmq_backend_names = [backend.name for backend in service.backends()]
provider = IBMProvider()
print(ibmq_backend_names)

try:
    import qb.core as qbc

    qbc_backend_names = ["qb-default", "qb-qdk1", "qb-nm1", "qb-nm2"]
except Exception:
    qbc = None
    qbc_backend_names = []

import json

print(qbc_backend_names)

import re


def qasm_correct(qc):
    text = qc.qasm()

    # Define the regular expression pattern to match scientific notation
    scientific_notation_pattern = r"\d+(\.\d+)?[eE][+-]?\d+"

    # Split the text into lines
    lines = text.split("\n")

    # Filter out lines that contain numbers in scientific notation
    filtered_lines = [line for line in lines if not re.search(scientific_notation_pattern, line)]

    # Join the filtered lines back into a single string
    result_text = "\n".join(filtered_lines)

    return result_text


class Tester:
    def __init__(self, backend):
        self.backend = backend
        if backend == 'aer-perfect':
            self.sim = Aer.get_backend('aer_simulator')
        elif backend in ibmq_backend_names:
            # get a real backend from a real provider
            print(f"acquiring data on {backend}...")
            ibmq_backend = provider.get_backend(backend)
            print(f"done")
            # generate a simulator that mimics the real quantum system with the latest calibration results
            self.sim = AerSimulator.from_backend(ibmq_backend)
        elif backend in qbc_backend_names:
            self.sim = qbc.session()
            # Set up meaningful defaults for session parameters
            self.sim.qb12()
            # Choose a simulator backend
            self.sim.acc = "aer"
            self.sim.noise = True

    def __call__(self, qc, shots=1024):
        if self.backend == 'aer-perfect' or self.backend in ibmq_backend_names:
            job = self.sim.run(transpile(qc, self.sim), shots=shots, memory=True)
            counts = job.result().get_counts()
        elif self.backend in qbc_backend_names:
            # Choose how many qubits to simulate
            self.sim.qn = qc.num_qubits
            # Choose how many 'shots' to run through the circuit
            self.sim.sn = shots
            # Define the quantum program to run (aka 'quantum kernel' aka 'quantum circuit')
            self.sim.instring = qasm_correct(qc)
            # my_sim.noise_model = qbc.NoiseModel("default", qc.num_qubits)
            backend = self.backend
            if backend == "qb-default": backend = "default"
            self.sim.noise_model = qbc.NoiseModel(backend, qc.num_qubits)
            self.sim.run()
            counts = json.loads(self.sim.out_raw[0][0])
        else:
            counts = {}
        return counts


class TesterGroup:
    def __init__(self):
        self.testers = {}

    def __call__(self, qc, backend='aer-perfect', shots=1024):
        if backend not in self.testers:
            self.testers[backend] = Tester(backend)
        return self.testers[backend](qc, shots=shots)


def score_counts(c1, c2, naive=False):
    all_keys = set(c1.keys()) | set(c2.keys())  # get all measured result options
    values = np.array([[c1.get(key, 0), c2.get(key, 0)] for key in all_keys])
    # print(values)
    if np.sum(values[:,1])== 0:
        return np.nan

    percentages = values / np.sum(values, axis=0)
    # print(percentages)
    diffs = percentages.T[1] - percentages.T[0]
    # print(diffs)
    if naive:
        score = np.sqrt(np.sum(diffs ** 2))
    else:
        score = np.sum(np.abs(diffs) / 2)
    return score


def my_random_circuit(nq, ng, identity=True):
    if not identity:
        qc = random_circuit(nq, ng, measure=False)
    else:
        qc = random_circuit(nq, ng // 2, measure=False)
        qc = qc.compose(qc.inverse())
    qc.measure_all()
    return qc


def test_on_random_circuits(tg, backends, nq=2, ng=2, nc=1, shots=1024, naive=False):
    circuits = [transpile(my_random_circuit(nq, ng, identity=not naive),
                          basis_gates=['id', 'ry', 'rx', 'cx', 'cy', 'cz', 'rz', 'x', 'y', 'z']) for _ in range(nc)]
    scores = {backend: [] for backend in backends}
    for qc in circuits:
        reference = tg(qc, shots=shots)
        for backend in backends:
            try:
                counts = tg(qc, backend=backend, shots=shots)
                score = score_counts(reference, counts, naive=naive)
            except Exception as e:
                if not "is greater than" in str(e):
                    print(f"on {backend}, {nq=}, {ng=}: {e}")
                score = np.nan
            scores[backend].append(score)
    for key in scores:
        scores[key] = np.array(scores[key])
    return scores
