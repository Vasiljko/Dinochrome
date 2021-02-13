class NodeGene:
    def __init__(self, type, id):
        #input node  -> 0
        #hidden_node -> 1
        #output_node -> 2
        self.type = type
        self.id = id

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id

    def getType(self):
        return self.type

    def getId(self):
        return self.id

    def Print(self):
        print(str(self.type)+" "+str(self.id))
