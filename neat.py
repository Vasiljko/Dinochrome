import numpy as np


class Agent:

    def __init__(self, input_layer_size, output_layer_size, parentA=None, parentB=None):
        self.input_layer_size = input_layer_size
        self.output_layer_size = output_layer_size

        # if unit is not made by cross over
        if parentA is None and parentB is None:

            # array of tuples (number, string) number is each neurons id
            # and string represents the type of neuron, can be one of: Sensor, Hidden, Output
            # self.node_genes = array(['1', 'sensor'],
            #                         ['2', 'output'],
            #                         ['3', 'hidden']])
            # this encoding for node_genes is not correct it should contain instances of Node class
            # it shouldn't be hard to change that when we figure out how feedforward works...
            self.node_genes = np.array([1, 'sensor'])
            # node_genes always start with sensor and output nodes, then hidden nodes follow
            for i in np.arange(2, self.input_layer_size + 1):
                new_sensor_node = (i, "sensor")
                self.node_genes = np.vstack([self.node_genes, new_sensor_node])
            for i in np.arange(self.input_layer_size + 1, self.input_layer_size + self.output_layer_size + 1):
                new_output_node = (i, "output")
                self.node_genes = np.vstack([self.node_genes, new_output_node])

            # numpy array, each row contains: in-node, out-node, weight_value, enable_bit, innovation number
            # if enable bit is True than connection is activated othervise it's not
            self.connection_genes = np.empty((0, 5), int) # empty array whose rows have 5-values needed for vstack to work


            # neat starts out from minimal structure ie. each sensor
            # node connects directly to every output node
            # this part of the code will also need to change a bit when
            # Node class is introduced
            local_innovation_number = 1
            for input_node in self.node_genes[:self.input_layer_size]:
                for output_node in self.node_genes[self.input_layer_size:self.input_layer_size+self.output_layer_size]:
                    # start with random weights in [-5, 5) I don't know how optimal this distribution is
                    random_weight = np.random.uniform(-5, 5)
                    enable_bit = 1 # each connection is activated
                    new_connection = [input_node[0], output_node[0], random_weight, enable_bit, local_innovation_number]
                    local_innovation_number += 1
                    self.connection_genes = np.vstack([self.connection_genes, new_connection])

        # if only one parrent is given copy genes from that parent
        elif parentA is not None and parentB is None:
            self.node_genes = parentA.node_genes.copy()
            self.connection_genes = parentA.connection_genes.copy()

        elif parentB is not None and parentA is None:
            self.node_genes = parentB.node_genes.copy()
            self.connection_genes = parentB.connection_genes.copy()

        else: # cross over
            pass

    def sigmoid(self, x):
        """
        Neat uses a modified sigmoidal
        transfer function
        """
        return 1 / (1 + np.exp(-4.9 * x))


# testing
agent = Agent(3, 2)
print(agent.node_genes)
print(agent.connection_genes, end="\n\n")
agent_copy = Agent(3, 2, agent)
print(agent_copy.node_genes)
print(agent_copy.connection_genes, end="\n\n")
agent_copyA = Agent(3, 2, parentA=agent)
print(agent_copyA.node_genes)
print(agent_copyA.connection_genes, end="\n\n")
agent_copyB = Agent(3, 2, parentB=agent)
# check that it is a different object as it should be
agent_copyB.connection_genes[2] = 1
print(agent_copyB.node_genes)
print(agent_copyB.connection_genes)


"""
more testing
agent1 = Agent(3, 1)
agent1.connection_genes = np.array([[1, 1, 4, 7, 1],
                                    [2, 2, 4, 7, 1],
                                    [3, 3, 4, 7, 1],
                                    [4, 2, 5, 7, 1],
                                    [5, 5, 4, 7, 1],
                                    [6, 1, 5, 7, 1],
                                    [7, 4, 5, 7, 1]])
"""