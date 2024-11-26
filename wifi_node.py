# wifi_node.py
import random
from algorithms import delay_based_algorithm, backoff_algorithm, qos_based_algorithm, rank_based_algorithm

class WifiNode:
    def __init__(self, env, node_id, access_point, qos_threshold=0.01, algorithm='delay_based'):
        self.env = env
        self.node_id = node_id
        self.remaining_energy = 1000
        self.delay = 0.0
        self.cw = 31
        self.access_point = access_point
        self.transmissions = 0
        self.collisions = 0
        self.qos_threshold = qos_threshold
        self.algorithm = algorithm
        self.last_logged_energy = self.remaining_energy
        self.action = env.process(self.run())

    def calculate_delay(self):
        slot_time = 0.000009
        data_rate = 54e6
        packet_size = 512 * 8

        backoff_slots = random.randint(0, self.cw)
        backoff_time = backoff_slots * slot_time
        transmission_time = packet_size / data_rate

        self.delay = backoff_time + transmission_time

    def energy_consumption(self):
        transmission_time = (128 / self.cw)
        energy_per_transmission = 10
        energy_consumed = energy_per_transmission * transmission_time * (1 + self.transmissions)
        self.remaining_energy = max(100, self.remaining_energy - energy_consumed)

    def run(self):
        while self.remaining_energy > 100:
            yield self.env.timeout(random.uniform(0.005, 0.01))
            self.transmissions += 1

            self.calculate_delay()

            success = yield self.env.process(self.access_point.handle_transmission(self, self.remaining_energy))
            if success:
                # Choose the appropriate algorithm
                if self.algorithm == 'delay_based':
                    self.cw = delay_based_algorithm(self.cw, self.delay, self.qos_threshold)
                elif self.algorithm == 'backoff':
                    self.cw = backoff_algorithm(self.cw, self.collisions)
                elif self.algorithm == 'qos_based':
                    self.cw = qos_based_algorithm(
                        self.cw, self.delay, self.qos_threshold, self.remaining_energy, self.access_point.nodes
                    )
                elif self.algorithm == 'rank_based':
                    self.cw = rank_based_algorithm(
                        self.cw, self.delay, self.qos_threshold, self.remaining_energy, self.access_point.nodes
                    )
            else:
                self.collisions += 1

            self.energy_consumption()

    def update_last_logged_energy(self):
        self.last_logged_energy = self.remaining_energy

    def get_last_logged_energy(self):
        return self.last_logged_energy
