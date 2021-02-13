from NodeGene import NodeGene
from ConnectionGene import ConnectionGene
import Innovation
import numpy as np
import random


class Genome:

    def __init__(self):
        # List of connections -> using ConnectionGene class
        self.connections = []

        # List of nodes -> using NodeGene class
        self.nodes = []

    def getNodes(self):
        return self.nodes

    def getConnections(self):
        return self.connections

    def addNode(self, node):
        self.nodes.append(node)

    def addConnection(self, connection):
        self.connections.append(connection)


    def add_connection(self):
        random_index1 = random.randint(0,len(self.nodes)-1)
        while True:
            random_index2 = random.randint(0,len(self.nodes)-1)
            if random_index2 != random_index1: break

        node1 = self.nodes[random_index1]
        node2 = self.nodes[random_index2]
        weight = 2 * random.random() - 1

        #MIGHT NEED IN FUTURE
        reversed_connection = False

        if node1.getType() == 1 and node2.getType() == 0:
            reversed_connection = True
        if node1.getType() == 2 and node2.getType() == 1:
            reversed_connection = True
        if node1.getType() == 0 and node2.getType() == 2:
            reversed_connection = True


        connection_exists = False

        for connection in self.connections:
            if connection.getInNode() == node1.getId() and connection.getOutNode == node2.getId():
                connection_exists = True
            elif connection.getInNode() == node2.getId() and connection.getOutNode == node1.getId():
                connection_exists = True

        if not connection_exists:
            if not reversed_connection:
                self.connections.append(ConnectionGene(node1.getId(), node2.getId(), weight, True, Innovation.getNewInnovation()))
            else:
                self.connections.append(ConnectionGene(node2.getId(), node1.getId(), weight, True, Innovation.getNewInnovation()))


    def add_node(self):
        random_connection_index = random.randint(0,len(self.connections)-1)
        connection = self.connections[random_connection_index]

        inNode = connection.getInNode()
        outNode = connection.getOutNode()
        current_weight = connection.weight

        # Disable current conenction
        connection.expressed = False


        # Add node in hidden layer -> type = 1
        id = len(self.nodes)
        self.nodes.append(NodeGene(1, id))


        # Add connection start_node -> new_one
        self.connections.append(ConnectionGene(inNode, id, 1.0, True, Innovation.getNewInnovation()))

        # Add connection new_one -> end_node
        self.connections.append(ConnectionGene(id, outNode, current_weight, True, Innovation.getNewInnovation()))


    # Assuming that Parent 1 is fitter than Parent 2
    def crossover(self, parent1, parent2):
        child = Genome()

        nodes1 = parent1.getNodes()
        for node in nodes1:
            child.addNode(node)

        connections1 = parent1.getConnections()
        connections2 = parent2.getConnections()

        # Do the Crossover

        i,j = 0,0
        while i<len(connections1) or j<len(connections2):
            if i == len(connections1):
                # Do nothing, because Parent 1 is fitter than parent 2
                j+=1
            elif j == len(connections2):
                # Excess Gene of Parent 1
                child.addConnection(connections1[i])
                i+=1
            else:
                if connections1[i].getInnovation() == connections2[j].getInnovation():
                    r = (random.random())
                    print(r)
                    r=round(r)
                    print(r)
                    child.addConnection(connections1[i] if r==0 else connections2[j])
                    i+=1
                    j+=1
                elif connections1[i].getInnovation() < connections2[j].getInnovation():
                    # Disjoint Gene of Parent 1
                    child.addConnection(connections1[i])
                    i+=1
                else:
                    # Do nothing, because Parent 1 is fitter than Parent 2
                    j+=1


        return child
