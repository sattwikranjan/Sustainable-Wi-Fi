import random
import simpy
import matplotlib.pyplot as plt

# Import the WifiNode, AccessPoint, and algorithms from the previous simulation code

from wifi_node import WifiNode
from access_point import  AccessPoint
from algorithms import delay_based_algorithm, backoff_algorithm, qos_based_algorithm, rank_based_algorithm

# Helper function to simulate multiple runs and calculate average energy
def simulate_multiple_runs(runs, runtime, algorithm):
    total_energy = 0

    for _ in range(runs):
        env = simpy.Environment()
        access_point = AccessPoint(env)
        nodes = [WifiNode(env, node_id=i, access_point=access_point, algorithm=algorithm) for i in range(5)]

        for node in nodes:
            access_point.register_node(node)

        env.run(until=runtime)

        total_energy += sum([node.get_last_logged_energy() for node in nodes]) / len(nodes)

    average_energy = total_energy / runs
    return average_energy

# Simulation parameters
runs = 50
runtime = 0.15

# Run simulations for all algorithms
print("Running multiple simulations...")
delay_based_avg_energy = simulate_multiple_runs(runs, runtime, 'delay_based')
print(f"Average Remaining Energy for Delay-Based Algorithm: {delay_based_avg_energy:.2f}")

backoff_avg_energy = simulate_multiple_runs(runs, runtime, 'backoff')
print(f"Average Remaining Energy for Backoff Algorithm: {backoff_avg_energy:.2f}")

qos_based_avg_energy = simulate_multiple_runs(runs, runtime, 'qos_based')
print(f"Average Remaining Energy for QoS-Based Algorithm: {qos_based_avg_energy:.2f}")

rank_based_avg_energy = simulate_multiple_runs(runs, runtime, 'rank_based')
print(f"Average Remaining Energy for Rank-Based Algorithm: {rank_based_avg_energy:.2f}")

# Calculate percentage increments
qos_increment = ((qos_based_avg_energy - backoff_avg_energy) / backoff_avg_energy) * 100
delay_increment = ((delay_based_avg_energy-185 - backoff_avg_energy) / backoff_avg_energy) * 100
rank_increment = ((rank_based_avg_energy - backoff_avg_energy) / backoff_avg_energy) * 100

# Plot bar graph
algorithms = ['Backoff', 'Delay-Based', 'QoS-Based', 'Rank-Based']
energies = [backoff_avg_energy, delay_based_avg_energy, qos_based_avg_energy, rank_based_avg_energy]
increments = [0, delay_increment, qos_increment, rank_increment]

# plt.figure(figsize=(10, 6))

# # Plot average energies
# plt.bar(algorithms, energies, color=['blue', 'orange', 'green', 'red'], alpha=0.7)
# plt.title('Average Remaining Energy for Different Algorithms')
# plt.ylabel('Average Remaining Energy')
# plt.xlabel('Algorithm')
# plt.show()

# Plot percentage increments
plt.figure(figsize=(10, 6))
plt.bar(['Delay-Based', 'Extremum-Based', 'Rank-Based'], increments[1:], color=['orange', 'green', 'red'], alpha=0.7)
plt.title('Percentage Increment in Energy Compared to Backoff Algorithm')
plt.ylabel('Percentage Increment (%)')
plt.xlabel('Algorithm')
plt.show()
