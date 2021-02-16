INNOVATION = 0
dict = {}


def getNewInnovation(node_in, node_out):
    global INNOVATION

    if (node_in,node_out) in dict:
        return dict[(node_in,node_out)]

    INNOVATION += 1
    dict[(node_in,node_out)] = INNOVATION

    return dict[(node_in,node_out)]
