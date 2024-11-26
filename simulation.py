from simpy import Environment
from wifi_node import WifiNode
from access_point import AccessPoint
from algorithms import delay_based_algorithm, backoff_algorithm, qos_based_algorithm, rank_based_algorithm
import random

def simulate_wifi_environment(runtime, algorithm):
    env = Environment()
    access_point = AccessPoint(env)
    nodes = [WifiNode(env, node_id=i, access_point=access_point, algorithm=algorithm) for i in range(5)]

    for node in nodes:
        access_point.register_node(node)

    env.run(until=runtime)

    total_energy = sum([node.get_last_logged_energy() for node in nodes])
    average_energy = total_energy / len(nodes)
    print(f"\nAverage Remaining Energy of all Nodes at the End of Simulation: {average_energy:.2f}")

# Run simulations
if __name__ == "__main__":
    print("Simulation with Delay-Based Algorithm:")
    simulate_wifi_environment(runtime=0.15, algorithm='delay_based')

    print("\nSimulation with Backoff Algorithm:")
    simulate_wifi_environment(runtime=0.15, algorithm='backoff')

    print("\nSimulation with Extremum-Based Algorithm:")
    simulate_wifi_environment(runtime=0.15, algorithm='qos_based')

    print("\nSimulation with Rank-Based Algorithm:")
    simulate_wifi_environment(runtime=0.15, algorithm='rank_based')
