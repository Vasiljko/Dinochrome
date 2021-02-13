class ConnectionGene:
    # in_node and out_node are ids of in and out node
    def __init__(self, in_node, out_node, weight, expressed, innovation_number):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.expressed = expressed
        self.innovation_number = innovation_number

    def getInNode(self):
        return self.in_node

    def getOutNode(self):
        return self.out_node

    def getWeight(self):
        return self.weight

    def isExpressed(self):
        return self.expressed

    def getInnovation(self):
        return self.innovation_number

    def Print(self):
        print(str(self.in_node)+" "+str(self.out_node)+" "+str(self.weight)+" "+str(self.innovation_number)+" "+str(self.expressed))
        return
