from ConnectionGene import ConnectionGene
import numpy as np


#TODO: connections_in should be filled in Genome class
#TODO: Maybe some more calculate functions should be implemented

#TODO: Should find a way to calculate all the outputs for each NodeGene and then calculate final outputs
# But, what about reccurent connections??
# Should implement distance from input nodes, and then distance is equal to maximum value of
# previous node's distance + 1


class NodeGene:
    def __init__(self, type, id):
        #input node  -> 0
        #hidden_node -> 1
        #output_node -> 2
        self.type = type
        self.id = id

        self.connections_in = []    # List of ConnectionGenes
        self.output = 0


    def __eq__(self, other):
        return self.type == other.type and self.id == other.id

    def calculate(self):
        s = 0
        for connection in self.connections_in:
            if connection.expressed == True:
                s += connection.in_node.output * connection.weight

        self.output = self.activation_function(s)


    def activation_function(self, x):
        return 1/(1+np.exp(-4.9*x))

    def getType(self):
        return self.type

    def getId(self):
        return self.id

    def copyNode(self):
        return NodeGene(self.type, self.id)

    def Print(self):
        print(str(self.type)+" "+str(self.id))
