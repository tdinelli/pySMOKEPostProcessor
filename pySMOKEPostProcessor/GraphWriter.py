import networkx as nx
import matplotlib.pyplot as plt

class GrapWirter:

    def __init__(self, firstNames, secondNames, thickness, label):
        
        self.G = nx.DiGraph()
        self.NodesNames = []
        [self.NodesNames.append(x) for x in firstNames if x not in self.NodesNames]
        
        self.edgeStart = firstNames
        self.edgeEnd = secondNames
        self.tck = thickness
        self.edgeLabel = label

        self.AddEdges()
        widths = nx.get_edge_attributes(self.G, 'label')
        print(widths)
        """
        self.AddNodes()

        nodelist = self.G.nodes()
        print(nodelist)
        """
    def CreateGraph(self):
        pass

    def AddNodes(self):
        for name in self.NodesNames:
            self.G.add_nodes_from([
                (name,{"color": "green"})
            ])

    def AddEdges(self):
    
        for j in range(len(self.edgeStart)):
            self.G.add_edges_from([
                (self.edgeStart[j], self.edgeEnd[j], {"color": "blue", 
                                                    "weight": self.tck[j], 
                                                    "label": str(round(self.edgeLabel[j],3)) + " %"})
            ])