import numpy as np

class Agent:

    def __init__(self, input_layer_size, output_layer_size):
        self.input_layer_size = input_layer_size
        self.output_layer_size = output_layer_size

        # array of tuples (number, string) number is each neurons id
        # and string represents the type of neuron, can be one of: Sensor, Hidden, Output
        # self.node_genes = array(['1', 'sensor'],
        #                         ['2', 'output'],
        #                         ['3', 'hidden']])
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
        self.connection_genes = np.array([])

    def sigmoid(self, x):
        """
        Neat uses a modified sigmoidal
        transfer function
        """
        return 1 / (1 + np.exp(-4.9 * x))


"""
testing
agent1 = Agent(3, 1)
agent1.connection_genes = np.array([[1, 1, 4, 7, 1],
                                    [2, 2, 4, 7, 1],
                                    [3, 3, 4, 7, 1],
                                    [4, 2, 5, 7, 1],
                                    [5, 5, 4, 7, 1],
                                    [6, 1, 5, 7, 1],
                                    [7, 4, 5, 7, 1]])
"""