from NodeGene import NodeGene
from ConnectionGene import ConnectionGene
import Innovation
import numpy as np
import random


# TODO: Crossover and compatibility distance should be changed (current complexity is O(NlogN) where N is number of ConnectionGenes
# TODO: In order to decrease it to linear complexity, the way of storing ConenctionGenes should be changed, i.e. we should use dictionaries

# Changed getConnections() and getNodes(). They are not using deepcopy anymore


class Genome:

    def __init__(self):
        self.connections = []   # List of connections -> using ConnectionGene class

        self.nodes = []         # List of nodes -> using NodeGene class

    def getNodes(self):
        new_nodes = []
        for node in self.nodes:
            new_nodes.append(NodeGene(node.type, node.id))
        return new_nodes

    def getConnections(self):
        new_connections = []
        for connection in self.connections:
            new_connections.append(ConnectionGene(connection.in_node, connection.out_node, connection.weight, connection.expressed, connection.innovation_number))
        return new_connections

    def addNode(self, node):
        self.nodes.append(node)

    def addConnection(self, connection):
        self.connections[connection.innovation_number] = ConnectionGene(connection.in_node, connection.out_node, connection.weight, connection.expressed, connection.innovation_number)


    def mutation(self):
        if random.random()>0.8:     # There is 80% change that mutation is going to happen
            return

        # 90% chance for weight to be uniformly perturbed
        # 10% chance of being assigned a new value
        for connection in self.connections:
            if random.random()<0.9:
                connection.weight = connection.weight*(4*random.random() - 2)
            else:
                connection.weight = 4*random.random() - 2

    def add_connection(self,max_iterations):
        iteration = 0

        # It also breaks when connection is found
        while iteration < max_iterations:
            iteration += 1

            random_index1 = random.randint(0, len(self.nodes) - 1)
            random_index2 = random.randint(0,len(self.nodes)-1)

            node1 = self.nodes[random_index1]
            node2 = self.nodes[random_index2]
            weight = 2 * random.random() - 1

            # There are no connections between input nodes, same for output nodes
            if node1.getType() == 0 and node2.getType() == 0:
                continue
            if node1.getType() == 2 and node2.getType() == 2:
                continue


            reversed_connection = False

            if node1.getType() == 1 and node2.getType() == 0:
                reversed_connection = True
            if node1.getType() == 2 and node2.getType() == 1:
                reversed_connection = True
            if node1.getType() == 0 and node2.getType() == 2:
                reversed_connection = True


            connection_exists = False

            for connection in self.connections:
                if connection.getInNode() == node1.getId() and connection.getOutNode() == node2.getId():
                    connection_exists = True
                elif connection.getInNode() == node2.getId() and connection.getOutNode() == node1.getId():
                    connection_exists = True


            if connection_exists:
                continue

            if not reversed_connection:
                new_connection = ConnectionGene(node1.getId(),node2.getId(),weight,True,Innovation.getNewInnovation(node1.getId(),node2.getId()))
                self.addConnection(new_connection)
            else:
                new_connection = ConnectionGene(node2.getId(),node1.getId(),weight,True,Innovation.getNewInnovation(node2.getId(),node1.getId()))
                self.addConnection(new_connection)

            # Added new connection
            break

    def add_node(self):
        random_connection_index = random.randint(0,len(self.connections)-1)
        connection = self.connections[random_connection_index]

        inNode = connection.getInNode()
        outNode = connection.getOutNode()
        current_weight = connection.weight

        # Disable current conenction
        connection.expressed = False


        # Add node in hidden layer -> type = 1
        id = len(self.nodes)+1
        self.nodes.append(NodeGene(1, id))


        # Add connection start_node -> new_one
        self.connections.append(ConnectionGene(inNode, id, 1.0, True, Innovation.getNewInnovation(inNode, id)))

        # Add connection new_one -> end_node
        self.connections.append(ConnectionGene(id, outNode, current_weight, True, Innovation.getNewInnovation(id, outNode)))


    # Assuming that Parent 1 is fitter than Parent 2
    def crossover(self, parent1, parent2):
        child = Genome()

        nodes1 = parent1.getNodes()
        for node in nodes1:
            child.addNode(node)

        connections1 = sorted(parent1.getConnections())
        connections2 = sorted(parent2.getConnections())

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
                    if (connections1[i].isExpressed() and connections2[j].isExpressed()) or (not connections1[i].isExpressed() and not connections2[j].isExpressed()):
                        r = round(random.random())
                        child.addConnection(connections1[i] if r==0 else connections2[j])
                    else:
                        r = random.random()

                        # 75% change of inheriting disabled connection gene
                        if r<0.75:
                            child.addConnection(connections1[i] if not connections1[i].isExpressed() else connections2[j])
                        else:
                            child.addConnection(connections1[i] if connections1[i].isExpressed() else connections2[j])

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


    def compatibility_distance(self, g1, c1, c2, c3):
        matching, disjoint, excess, weight = 0, 0, 0, 0

        i, j = 0, 0
        connections1 = sorted(self.getConnections())
        connections2 = sorted(g1.getConnections())

        while i < len(connections1) or j < len(connections2):
            if i == len(connections1):  # No gene from g2 can be matched
                excess += 1
                j += 1
            elif j == len(connections2):  # No gene from g1 can be matched
                excess += 1
                i += 1
            else:
                if connections1[i].getInnovation() == connections2[j].getInnovation():
                    matching += 1
                    weight += abs(connections1[i].weight - connections2[j].weight)

                    i += 1
                    j += 1
                elif connections1[i].getInnovation() < connections2[j].getInnovation():
                    disjoint += 1
                    i += 1
                else:
                    disjoint += 1
                    j += 1

        N = max(len(self.connections), len(g1.connections))
        N = 1 if N < 20 else N

        W = weight / matching if matching != 0 else 0

        print(matching, disjoint, excess)
        return c1 * excess / N + c2 * disjoint / N + c3 * W





