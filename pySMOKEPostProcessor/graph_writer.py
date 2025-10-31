from graphviz import Digraph


class GraphWriter:
    def __init__(self, flux_type: str):  # , first: str, last: str):
        self.G = Digraph("Flux Analysis", node_attr={"shape": "circle"}, engine="dot")  # filename=''

        self.flux_type = flux_type
        if flux_type == "production":
            self.color = "blue"
        elif flux_type == "destruction":
            self.color = "red"
        else:
            raise ValueError("Unknown type of flux analysis, available are: production | destruction")

    def create_graph(self, edge_start, edge_end, thickness, label):
        # There is a possible bug I need to do a check
        # on list edge_start edge_end intersection cause it
        # can generate bugs when for instance end nodes
        # are just accumulation point
        NodesNames = list(set(edge_start + edge_end))
        # this is not the best
        # idx_first = NodesNames.index(self._first)
        # NodesNames.insert(0, NodesNames.pop(idx_first))
        # idx_last = NodesNames.index(self._last)
        # NodesNames.insert(len(NodesNames) - 1, NodesNames.pop(idx_last))

        self.add_nodes(NodesNames)
        self.add_edges(edge_start, edge_end, thickness, label)
        return self.G

    def add_nodes(self, NodesNames):
        self._map_node_names = {}
        for i, name in enumerate(NodesNames):
            self._map_node_names[name] = i
            self.G.node(str(i), name)

    def add_edges(self, edge_start, edge_end, tck, edge_label):
        # print(self._map_node_names)
        for i, start in enumerate(edge_start):
            tickness = tck[i]
            map_name_start = str(self._map_node_names[start])
            map_name_end = str(self._map_node_names[edge_end[i]])
            if edge_label[i] > 10:
                label_str = "   " + str(round(edge_label[i], 1)) + " %"
            elif edge_label[i] > 1:
                label_str = "   " + str(round(edge_label[i], 2)) + " %"
            elif edge_label[i] > 0.1:
                label_str = "   " + str(round(edge_label[i], 3)) + " %"
            elif edge_label[i] > 0.01:
                label_str = "   " + str(round(edge_label[i], 4)) + " %"
            else:
                label_str = "   " + str(format(edge_label[i], ".2E")) + " %"

            if self.flux_type == "destruction":
                self.G.edge(
                    map_name_start,
                    map_name_end,
                    color=self.color,
                    weight=str(tickness),
                    label=label_str,
                    penwidth=str(tickness),
                )
            elif self.flux_type == "production":
                # Arrows have to point the opposite direction
                self.G.edge(
                    map_name_end,
                    map_name_start,
                    label=label_str,
                    color=self.color,
                    weight=str(tickness),
                    penwidth=str(tickness),
                )
