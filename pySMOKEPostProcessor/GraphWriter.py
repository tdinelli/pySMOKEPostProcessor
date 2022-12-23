import networkx as nx

"""
DESCRIPTION: TODO
"""

class GraphWriter:

    def __init__(self, fluxanalysistype: str):
        
        self.G = nx.DiGraph()
        self.fluxanalysistype_ = fluxanalysistype
        if(fluxanalysistype == 'production'):
            self.color = "blue"
        elif(fluxanalysistype == 'destruction'):
            self.color = "red"

    def CreateGraph(self, edgeStart, edgeEnd, thickness, label):
        
        NodesNames = []
        [NodesNames.append(x) for x in edgeStart if x not in NodesNames]
        
        self.AddNodes(NodesNames)
        self.AddEdges(edgeStart, edgeEnd, thickness, label)

        self.G.graph['graph'] = {"overlap": "false", "fontsize":14} # settings just for Graphviz style visualization
        self.G.graph['node'] = {"shape": "circle"} # settings just for Graphviz style visualization
        
        return self.G

    def AddNodes(self, NodesNames):
        for name in NodesNames:
            self.G.add_nodes_from([
                (name,{"color": "black"})
            ])

    def AddEdges(self, edgeStart, edgeEnd, tck, edgeLabel):
        
        for j in range(len(edgeStart)):
            
            if(edgeLabel[j] > 10):
                label_str = "   " + str(round(edgeLabel[j],1)) + " %"
            elif(edgeLabel[j]>1):
                label_str = "   " + str(round(edgeLabel[j],2)) + " %"
            elif(edgeLabel[j]>0.1):
                label_str = "   " + str(round(edgeLabel[j],3)) + " %"
            elif(edgeLabel[j]>0.01):
                label_str = "   " + str(round(edgeLabel[j],4)) + " %"
            else:
                label_str = "   " + str(format(edgeLabel[j],'.2E')) + " %"

            if(self.fluxanalysistype_ == 'destruction'):
                self.G.add_edges_from([
                        (edgeStart[j], 
                        edgeEnd[j], {"color": self.color, 
                                    "weight": tck[j], 
                                    "label": label_str,
                                    "penwidth": tck[j]})
                ])
            elif(self.fluxanalysistype_ == 'production'):
                # Arrows have to point the opposite direction
                self.G.add_edges_from([
                        (edgeEnd[j], 
                        edgeStart[j], {"color": self.color, 
                                    "weight": tck[j], 
                                    "label": label_str,
                                    "penwidth": tck[j]})
                ])    

        
