from graphviz import Digraph

"""
DESCRIPTION: TODO
"""


class GraphWriter:

    def __init__(self, fluxAnalysisType: str, first: str, last: str):
        self.G = Digraph('Flux Analysis',
                         node_attr={'shape': 'circle'},
                         engine='dot')  # filename=''

        self.fluxAnalysisType_ = fluxAnalysisType
        if (fluxAnalysisType == 'production'):
            self.color = "blue"
        elif (fluxAnalysisType == 'destruction'):
            self.color = "red"
        else:
            raise ValueError('Unknown type of flux analysis, available are: production | destruction')

        self._first = first
        self._last = last

    def CreateGraph(self, edgeStart, edgeEnd, thickness, label):
        # There is a possible bug I need to do a check
        # on list edgeStart edgeEnd intersection cause it
        # can generate bugs when for instance end nodes
        # are just accumulation point
        NodesNames = list(set(edgeStart + edgeEnd))
        # this is not the best
        idx_first = NodesNames.index(self._first)
        NodesNames.insert(0, NodesNames.pop(idx_first))
        idx_last = NodesNames.index(self._last)
        NodesNames.insert(len(NodesNames) - 1, NodesNames.pop(idx_last))

        self.AddNodes(NodesNames)
        self.AddEdges(edgeStart, edgeEnd, thickness, label)
        return self.G

    def AddNodes(self, NodesNames):
        self._map_node_names = {}
        for i, name in enumerate(NodesNames):
            self._map_node_names[name] = i
            self.G.node(str(i), name)

    def AddEdges(self, edgeStart, edgeEnd, tck, edgeLabel):
        # print(self._map_node_names)
        for i, start in enumerate(edgeStart):
            tickness = tck[i]
            map_name_start = str(self._map_node_names[start])
            map_name_end = str(self._map_node_names[edgeEnd[i]])
            if (edgeLabel[i] > 10):
                label_str = "   " + str(round(edgeLabel[i], 1)) + " %"
            elif (edgeLabel[i] > 1):
                label_str = "   " + str(round(edgeLabel[i], 2)) + " %"
            elif (edgeLabel[i] > 0.1):
                label_str = "   " + str(round(edgeLabel[i], 3)) + " %"
            elif (edgeLabel[i] > 0.01):
                label_str = "   " + str(round(edgeLabel[i], 4)) + " %"
            else:
                label_str = "   " + str(format(edgeLabel[i], '.2E')) + " %"

            if (self.fluxAnalysisType_ == 'destruction'):
                self.G.edge(map_name_start,
                            map_name_end,
                            color=self.color,
                            weight=str(tickness),
                            label=label_str,
                            penwidth=str(tickness))
            elif (self.fluxAnalysisType_ == 'production'):
                # Arrows have to point the opposite direction
                self.G.edge(map_name_end,
                            map_name_start,
                            label=label_str,
                            color=self.color,
                            weight=str(tickness),
                            penwidth=str(tickness))
