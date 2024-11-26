import random
class AccessPoint:
    def __init__(self, env):
        self.env = env
        self.channel_busy = False
        self.nodes = []

    def register_node(self, node):
        self.nodes.append(node)

    def handle_transmission(self, node, remaining_energy):
        node.update_last_logged_energy()
        if self.channel_busy:
            # print(f"{self.env.now:.4f} - Node {node.node_id}: Collision detected, CW={node.cw}, Energy={remaining_energy:.2f}")
            yield self.env.timeout(random.uniform(0.001, 0.005))
            return False
        else:
            self.channel_busy = True
            # print(f"{self.env.now:.4f} - Node {node.node_id}: Successfully transmitted, CW={node.cw}, Energy={remaining_energy:.2f}")
            yield self.env.timeout(random.uniform(0.001, 0.005))
            self.channel_busy = False
            return True
