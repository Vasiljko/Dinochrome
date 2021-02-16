from NodeGene import NodeGene
from ConnectionGene import ConnectionGene
import Innovation
import numpy as np
import random


# FIXED: Crossover and compatibility distance should be changed (current complexity is O(NlogN) where N is number of ConnectionGenes
# FIXED: In order to decrease it to linear complexity, the way of storing ConenctionGenes should be changed, i.e. we should use dictionaries

# Changed getConnections() and getNodes(). They are not using deepcopy anymore


class Genome:

    def __init__(self):
        self.connections = {}   # Dictionary of connections -> using ConnectionGene class
                                # { Innovation number: ConnectionGene }

        self.nodes = []         # List of nodes -> using NodeGene class

    def getNodes(self):
        new_nodes = []
        for node in self.nodes:
            new_nodes.append(NodeGene(node.type, node.id))
        return new_nodes

    def getConnections(self):
        new_connections = {}
        for connection in self.connections.values():
            new_connections[connection.innovation_number] = ConnectionGene(connection.in_node, connection.out_node, connection.weight, connection.expressed, connection.innovation_number)
        return new_connections

    def addNode(self, node):
        self.nodes.append(NodeGene(node.type, node.id))

    def addConnection(self, connection):
        self.connections[connection.innovation_number] = ConnectionGene(connection.in_node, connection.out_node, connection.weight, connection.expressed, connection.innovation_number)


    def mutation(self):
        if random.random()>0.8:     # There is 80% change that mutation is going to happen
            return

        # 90% chance for weight to be uniformly perturbed
        # 10% chance of being assigned a new value
        for innovation in self.connections.keys():
            if random.random()<0.9:
                self.connections[innovation].weight = self.connections[innovation].weight*(4*random.random() - 2)
            else:
                self.connections[innovation].weight = 4*random.random() - 2

    def add_connection(self,max_iterations = 100):
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

            for connection in self.connections.values():
                if connection.in_node.id == node1.getId() and connection.out_node.id == node2.getId():
                    connection_exists = True
                elif connection.in_node.id == node2.getId() and connection.out_node.id == node1.getId():
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
        innovation = random.choice(list(self.connections.keys()))
        connection = self.connections[innovation]

        inNode = connection.getInNode()
        outNode = connection.getOutNode()
        current_weight = connection.weight

        # Disable current conenction
        connection.expressed = False

        # Add node in hidden layer -> type = 1
        id = len(self.nodes)+1
        self.nodes.append(NodeGene(1, id))


        # Add connection start_node -> new_one
        new_innovation = Innovation.getNewInnovation(inNode.id, id)
        self.connections[new_innovation] = ConnectionGene(inNode.id, id, 1.0, True, new_innovation)

        # Add connection new_one -> end_node
        new_innovation = Innovation.getNewInnovation(inNode.id, id)
        self.connections[new_innovation] = ConnectionGene(id, outNode.id, current_weight, True, new_innovation)


    # Assuming that Parent 1 is fitter than Parent 2
    def crossover(self, parent1, parent2):
        child = Genome()

        nodes1 = parent1.getNodes()
        for node in nodes1:
            child.addNode(node)

        for innovation in parent1.connections.keys():
            if innovation in parent2.connections:    # Matching genes
                connection1 = parent1.connections[innovation]
                connection2 = parent2.connections[innovation]

                if (connection1.isExpressed() and connection2.isExpressed()) or (not connection1.isExpressed() and not connection2.isExpressed()):
                    r = round(random.random())
                    child.addConnection(connection1 if r == 0 else connection2)
                else:
                    r = random.random()

                    # 75% change of inheriting disabled connection gene
                    if r < 0.75:
                        child.addConnection(connection1 if not connection1.isExpressed() else connection2)
                    else:
                        child.addConnection(connection1 if connection1.isExpressed() else connection2)
            else:
                child.addConnection(parent1.connections[innovation])

        return child


    def compatibility_distance(self, g1, c1, c2, c3):
        matching, disjoint, excess, weight = 0, 0, 0, 0

        minimum_innovation1 = max(list(self.connections.keys()))
        minimum_innovation2 = max(list(g1.connections.keys()))
        minimum_innovation = min(minimum_innovation1, minimum_innovation2)

        for innovation in self.connections.keys():
            if innovation in g1.connections:
                matching += 1
                weight += abs(self.connections[innovation].weight - g1.connections[innovation].weight)
            elif innovation <= minimum_innovation:
                disjoint += 1
            else:
                excess += 1

        for innovation in g1.connections.keys():
            if innovation in self.connections:
                pass
            elif innovation <= minimum_innovation:
                disjoint += 1
            else:
                excess += 1

        N = max(len(self.connections), len(g1.connections))
        N = 1 if N < 20 else N

        W = weight / matching if matching != 0 else 0

        return c1 * excess / N + c2 * disjoint / N + c3 * W
