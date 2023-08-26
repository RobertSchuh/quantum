import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from tqdm import trange

# Create the "plots" directory if it doesn't exist
if not os.path.exists("plots"):
    os.makedirs("plots")


def yes_or_no(question):
    while True:
        choice = input(question + " (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")


# friction = yes_or_no("Use air friction?")
friction = True

if friction:
    prefix = "with air resistance"
    pre_short = "f"
else:
    prefix = "in vacuum"
    pre_short = "v"

# Constants
# For air drag calculations
mass = 0.05  # 50 g
cd = 0.7
r = 0.068 / 2  # 6.8 cm diameter
rho = 1.293  # kg/m³ air density
gamma = 0.5 * rho * cd * np.pi * r ** 2

# For pull-in process
original_r = 1
target_r = 0.1
# pull_speed = 0.05  # 5 cm/sec
pull_speed = 0.1 # 90 cm/sec
# define r(t) function for pull-in
desired_r = lambda t: np.max([original_r - np.max([0, pull_speed * (t - 3)]), target_r])

# initial velocity
original_RPM = 120
initial_position = np.array([original_r, 0.0])
initial_velocity = np.array([0.0, original_RPM / 60 * (2 * np.pi * original_r)])

# simulation settings
t_step = 1e-4  # smaller t_step is more accurate
# total_t = 50  # seconds
total_t = 25
ani_t = 25

print(f"{gamma=}")
if not friction:
    gamma = 0


class ForcePID:
    # regulates force on string for pull-in process, basic PID controller
    def __init__(self, f, kP=0, kI=0, kD=0):
        self.kP, self.kI, self.kD = kP, kI, kD
        self.rs = []
        self.ts = []
        self.errors = []
        self.desiredFunc = f
        self.integral = 0

    def __call__(self, r, t):
        error = r - self.desiredFunc(t)

        P = self.kP * error
        if len(self.ts) > 0:
            self.integral += (t - self.ts[-1]) * error * self.kI
            D = self.kD * (error - self.errors[-1]) / (t - self.ts[-1])
        else:
            D = 0, 0
        I = self.integral

        self.rs.append(r)
        self.ts.append(t)
        self.errors.append(error)

        # print(error, P, I, D)

        return P + I + D


forceStrength = ForcePID(desired_r, kP=25000, kI=100000, kD=1)


# Forces
def total_force(position, velocity, t):
    # air drag
    force1 = - gamma * velocity * np.linalg.norm(velocity)
    # string force
    force2 = - position / np.linalg.norm(position) * forceStrength(np.linalg.norm(position), t)
    return force1 + force2


# Initialize arrays to store data
num_steps = int(total_t / t_step)
positions = np.zeros((num_steps, 2))
velocities = np.zeros((num_steps, 2))
forces = np.zeros((num_steps, 2))
time = np.arange(num_steps) * t_step

# Initial conditions
positions[0] = initial_position
velocities[0] = initial_velocity

# Euler-Cromer integration
for i in trange(1, num_steps):
    force = total_force(positions[i - 1], velocities[i - 1], i * t_step)
    acceleration = force / mass
    velocities[i] = velocities[i - 1] + acceleration * t_step
    positions[i] = positions[i - 1] + velocities[i] * t_step
    forces[i] = force

# calculate observables
L = np.cross(positions, mass * velocities)
E = mass / 2 * np.sum(velocities ** 2, axis=1)

r = np.hypot(positions[:, 0], positions[:, 1])
theta = np.arctan2(positions[:, 1], positions[:, 0])

omega = np.diff(theta) % (2 * np.pi) / t_step
# omega = np.cross(positions, velocities) / np.linalg.norm(positions, axis=1)**2
RPM = 60 * omega / (2 * np.pi)

# P = np.sum(forces * velocities, axis=1)
P = - np.linalg.norm(forces, axis=1)[:-1] * np.diff(r) / t_step
W = np.cumsum(P) * t_step

fig, axs = plt.subplots(3, 2, figsize=(10, 8))
fig.suptitle(f"Ball on String {prefix}")

for ax in axs.flatten():
    ax.grid(True)

axs[0, 0].plot(time, [desired_r(t) for t in time], label="desired", alpha=0.5, linestyle="--", color="green")
axs[0, 0].plot(time, r, label="real")
# axs[0, 0].set_xlabel("t [s]")
axs[0, 0].set_ylabel("r [m]")
axs[0, 0].set_ylim([0, 1.2 * np.max(r)])
axs[0, 0].legend()

axs[0, 1].plot(time, np.linalg.norm(velocities, axis=1))
# axs[0, 1].set_xlabel("t [s]")
axs[0, 1].set_ylabel("v [m/s]")
axs[0, 1].set_ylim([0, 1.1 * np.max(np.linalg.norm(velocities, axis=1))])

axs[1, 0].plot(time, np.linalg.norm(forces, axis=1))
# axs[1, 0].set_xlabel("t [s]")
axs[1, 0].set_ylabel("F [N]")
axs[1, 0].set_ylim([0, 1.1 * np.max(np.linalg.norm(forces, axis=1))])

axs[1, 1].plot(time[:-1], RPM)
# axs[1, 1].set_xlabel("t [s]")
axs[1, 1].set_ylabel("RPM")
axs[1, 1].set_ylim([0, 1.1 * np.max(RPM)])

axs[2, 0].plot(time, E, label="E_kin")
axs[2, 0].plot(time[:-1], W, label="W")
axs[2, 0].plot(time[:-1], E[:-1] - W, label="E_kin - W")

axs[2, 0].set_xlabel("t [s]")
axs[2, 0].set_ylabel("E [J]")
axs[2, 0].legend()

axs[2, 1].plot(time, L)
axs[2, 1].set_xlabel("t [s]")
axs[2, 1].set_ylabel("L [kg m²/s]")
axs[2, 1].set_ylim([0, 1.1 * np.max(L)])

# Animation
fig, ax = plt.subplots(figsize=(6, 6))
max_r = np.max(np.linalg.norm(positions, axis=1)) * 1.2
ax.set_xlim(-max_r, max_r)
ax.set_ylim(-max_r, max_r)
ax.set_aspect('equal')
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_title(f'Ball on String {prefix}')
ax.grid(True)

trajectory, = ax.plot([], [], 'g--', linewidth=0.5, alpha=0.5)  # Trajectory trace
line, = ax.plot([], [], 'b-', linewidth=1)  # Line connecting origin and ball
ball, = ax.plot([], [], 'bo', markersize=10)
velocity_arrow = ax.arrow(0, 0, 0, 0, color='red', width=0.01)
time_text = ax.text(-max_r + 0.15, max_r - 0.15, '', fontsize=12)  # Text to display simulation time

frame_skip = int(1 / 20 / t_step)


def init():
    line.set_data([], [])
    ball.set_data([], [])
    trajectory.set_data([], [])
    velocity_arrow.set_data(x=0, y=0, dx=0, dy=0)
    time_text.set_text('')
    return line, ball, trajectory, velocity_arrow, time_text


def update(frame):
    frame *= frame_skip
    position = positions[frame]
    velocity = velocities[frame] * 0.02

    if np.linalg.norm(velocity) > 0.5:
        velocity *= 0.5 / np.linalg.norm(velocity)
    assert np.linalg.norm(velocity) < 0.6

    ball.set_data(position)
    line.set_data([0, position[0]], [0, position[1]])
    trajectory.set_data(positions[:frame:(frame_skip // 20), 0], positions[:frame:(frame_skip // 20), 1])

    velocity_arrow.set_data(x=position[0], y=position[1], dx=velocity[0], dy=velocity[1])

    time_text.set_text(f't = {time[frame]:.1f}s')

    return line, ball, trajectory, velocity_arrow, time_text


# Initialize the animation
ani = FuncAnimation(fig, update, frames=int(num_steps / frame_skip * (ani_t / total_t)), init_func=init,
                    interval=1000 * t_step * frame_skip, blit=True)

plt.show()

# Create a separate figure for each plot and save it
fig1, ax1 = plt.subplots(figsize=(8, 6), dpi=300)
ax1.grid(True)
ax1.plot(time, [desired_r(t) for t in time], label="desired", alpha=0.5, linestyle="--", color="green")
ax1.plot(time, r, label="real")
ax1.set_xlabel("t [s]")
ax1.set_ylabel("r [m]")
ax1.set_ylim([0, 1.2 * np.max(r)])
ax1.set_title(f"Desired vs. Real Radius ({prefix})")
ax1.legend()
fig1.savefig(f"plots/desired_real_plot_{pre_short}.png")
plt.close(fig1)

fig2, ax2 = plt.subplots(figsize=(8, 6), dpi=300)
ax2.grid(True)
ax2.plot(time, np.linalg.norm(velocities, axis=1))
ax2.set_xlabel("t [s]")
ax2.set_ylabel("v [m/s]")
ax2.set_ylim([0, 1.1 * np.max(np.linalg.norm(velocities, axis=1))])
ax2.set_title(f"Velocity over Time ({prefix})")
fig2.savefig(f"plots/velocity_plot_{pre_short}.png")
plt.close(fig2)

fig3, ax3 = plt.subplots(figsize=(8, 6), dpi=300)
ax3.grid(True)
ax3.plot(time, np.linalg.norm(forces, axis=1))
ax3.set_xlabel("t [s]")
ax3.set_ylabel("F [N]")
ax3.set_ylim([0, 1.1 * np.max(np.linalg.norm(forces, axis=1))])
ax3.set_title(f"Force Magnitude over Time ({prefix})")
fig3.savefig(f"plots/force_plot_{pre_short}.png")
plt.close(fig3)

fig4, ax4 = plt.subplots(figsize=(8, 6), dpi=300)
ax4.grid(True)
ax4.plot(time[:-1], RPM)
ax4.set_xlabel("t [s]")
ax4.set_ylabel("RPM")
ax4.set_ylim([0, 1.1 * np.max(RPM)])
ax4.set_title(f"Rotations per Minute (RPM) ({prefix})")
fig4.savefig(f"plots/RPM_plot_{pre_short}.png")
plt.close(fig4)

fig5, ax5 = plt.subplots(figsize=(8, 6), dpi=300)
ax5.grid(True)
ax5.plot(time, E, label="Kinetic Energy")
ax5.plot(time[:-1], W, label="Work done")
ax5.plot(time[:-1], E[:-1] - W, label="Ekin - W")
ax5.set_xlabel("t [s]")
ax5.set_ylabel("E [J]")
ax5.set_title(f"Energy Analysis ({prefix})")
ax5.legend()
fig5.savefig(f"plots/energy_plot_{pre_short}.png")
plt.close(fig5)

fig6, ax6 = plt.subplots(figsize=(8, 6), dpi=300)
ax6.grid(True)
ax6.plot(time, L)
ax6.set_xlabel("t [s]")
ax6.set_ylabel("L [kg m²/s]")
ax6.set_ylim([0, 1.1 * np.max(L)])
ax6.set_title(f"Angular Momentum ({prefix})")
fig6.savefig(f"plots/angular_momentum_plot_{pre_short}.png")
plt.close(fig6)

print(f"saving {int(num_steps / frame_skip * 0.6)} frames")
# Save the animation to a video file
output_file = f'plots/video_{pre_short}.mp4'
ani.save(output_file, writer='ffmpeg', fps=20)
print("File write done!")
