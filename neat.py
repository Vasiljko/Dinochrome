import numpy as np


class Node:

    def __init__(self, node_id, node_type):
        self.node_id = node_id
        self.node_type = node_type  # sensor, hidden or output

        # weighted sum of activations of the neurons
        # that have outgoing connections to this node
        self.activation_sum = 0
        self.activation = 0  # = sigmoid(activation_sum)
        self.previous_activation = 0

        # list of nodes that have outgoing connections to this node
        self.incoming = []
        # list of nodes that this node sends signals to
        self.outgoing = []
        # weights for the outgoing connections, in the same order
        # as the nodes in self.outgoing
        self.outgoing_weights = []

    def sigmoid(self, x):
        """
        Neat uses a modified sigmoidal
        transfer function
        """
        return 1 / (1 + np.exp(-4.9 * x))


class Agent:

    def __init__(self, input_layer_size, output_layer_size, parentA=None, parentB=None):
        self.input_layer_size = input_layer_size
        self.output_layer_size = output_layer_size

        # if unit is not made by cross over
        if parentA is None and parentB is None:

            # each gene is a Node object which has node_id and node_type ("sensor", "hidden", "output")
            self.node_genes = []
            # node_genes always starts with sensor and output nodes, then hidden nodes follow
            for i in np.arange(1, self.input_layer_size + 1):
                self.node_genes.append(Node(i, "sensor"))
            for i in np.arange(self.input_layer_size + 1, self.input_layer_size + self.output_layer_size + 1):
                self.node_genes.append(Node(i, "output"))

            # numpy array, each row contains: in-node, out-node, weight_value, enable_bit, innovation number
            # if enable bit is 1 than connection is activated otherwise it's not
            self.connection_genes = np.empty((0, 5), int)  # empty array whose rows have 5-values needed for vstack

            # neat starts out from minimal structure ie. each sensor
            # node connects directly to every output node
            local_innovation_number = 1
            for input_node in self.node_genes[:self.input_layer_size]:
                for output_node in self.node_genes[self.input_layer_size:self.input_layer_size+self.output_layer_size]:
                    # normal distribution with mean 0 and standard deviation 1/3
                    # this means that 99.7% od the values will be between -1 and 1
                    random_weight = np.random.normal(0, 1/3)
                    enable_bit = 1  # each connection is activated
                    new_connection = [input_node.node_id, output_node.node_id, random_weight,
                                      enable_bit, local_innovation_number]
                    local_innovation_number += 1
                    self.connection_genes = np.vstack([self.connection_genes, new_connection])

        # if only one parent is given copy genes from that parent
        elif parentA is not None and parentB is None:
            self.node_genes = []
            for node in parentA.node_genes:
                # for each node_gene in parents node_genes append a new node_gene with the same id and type
                self.node_genes.append(Node(node.node_id, node.node_type))
            self.connection_genes = parentA.connection_genes.copy()

        elif parentB is not None and parentA is None:
            self.node_genes = []
            for node in parentB.node_genes:
                self.node_genes.append(Node(node.node_id, node.node_type))
            self.connection_genes = parentB.connection_genes.copy()

        else:  # cross over
            pass
        # for each connection add to the outgoing list of the In Node reference to the Out Node
        # as well as the connection weight to the In Node's outgoing_weights
        # and to the incoming list of the Out Node reference to the In Node
        for connection_gene in self.connection_genes:
            input_node, output_node, weight = connection_gene[0], connection_gene[1], connection_gene[2]
            self.node_genes[int(input_node) - 1].outgoing.append(self.node_genes[int(output_node) - 1])
            self.node_genes[int(input_node) - 1].outgoing_weights.append(weight)
            self.node_genes[int(output_node) - 1].incoming.append(self.node_genes[int(input_node) - 1])


agent = Agent(2, 2)
print(agent.node_genes)
print(agent.connection_genes)
for node in agent.node_genes:
    print(node.incoming, node.outgoing, node.outgoing_weights, end="\n"*2)


"""
# testing
agent = Agent(3, 2)
print(agent.node_genes)
print(agent.connection_genes, end="\n\n")
agent_copy = Agent(3, 2, agent)
print(agent_copy.node_genes[0].node_id)
agent_copy.connection_genes[2] = 5
agent_copy.node_genes[2] = Node(13, "hidden")
print(agent_copy.node_genes)
print(agent_copy.connection_genes, end="\n\n")
agent_copyA = Agent(3, 2, parentA=agent)
agent_copyA.node_genes[0].node_id = 99
print(agent_copyA.node_genes[0].node_id)
print(agent_copyA.node_genes)
print(agent_copyA.connection_genes, end="\n\n")
agent_copyB = Agent(3, 2, parentB=agent)
# check that it is a different object as it should be
agent_copyB.connection_genes[2] = 1
print(agent_copyB.node_genes[0].node_id)
print(agent_copyB.node_genes)
print(agent_copyB.connection_genes)
"""