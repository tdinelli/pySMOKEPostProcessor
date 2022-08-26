import networkx as nx
import matplotlib.pyplot as plt

class GrapWirter:

    def __init__(self):
        
        self.G = nx.DiGraph()
        
    def CreateGraph(self, edgeStart, edgeEnd, thickness, label):
        
        NodesNames = []
        [NodesNames.append(x) for x in edgeStart if x not in NodesNames]
        
        self.AddNodes(NodesNames)
        self.AddEdges(edgeStart, edgeEnd, thickness, label)
        
        return self.G

    def AddNodes(self, NodesNames):
        for name in NodesNames:
            self.G.add_nodes_from([
                (name,{"color": "green"})
            ])

    def AddEdges(self, edgeStart, edgeEnd, tck, edgeLabel):
    
        for j in range(len(edgeStart)):
            self.G.add_edges_from([
                    (edgeStart[j], 
                    edgeEnd[j], {"color": "blue", 
                                "weight": tck[j], 
                                "label": str(round(edgeLabel[j],3)) + " %"})
            ])