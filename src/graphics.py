import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D
from matplotlib.patches import ArrowStyle

from entities import TransportSystem
from ui.dialogs.config import GUIConfig
from ui.styles import colors


class GraphBuilder:
    def __init__(self, sys: TransportSystem, config: GUIConfig):
        self.sys = sys
        self.config = config

        self.proxies = []
        self.signs = []

    def graph(self) -> nx.Graph:
        g = nx.Graph()
        for node in self.sys.nodes:
            g.add_node(node.name)
            for other, road in node.linked.items():
                g.add_edge(node.name, other.name, weight=1 / road.dist, **road.__dict__)
        return g

    def _build_nodes(self, subp):
        node = self.config.cur_node

        labels = {n: n for n in self.g}
        if node:
            del labels[node.name]

        if self.config.show_labels:
            nx.draw_networkx_labels(self.g, self.pos, ax=subp, labels=labels, verticalalignment='center',
                                    bbox={'pad': 0.4, 'boxstyle': 'round', 'facecolor': colors['accent1']})
        else:
            nodes = [self.sys.parking.name]
            nx.draw_networkx_nodes(self.g, self.pos, ax=subp, nodelist=nodes, node_shape='o', node_size=100)
            self.proxies.append(Line2D(range(1), range(1), marker='o', lw=0))
            self.signs.append('стоянка')

            nodes = [n.name for n in self.sys.warehouses]
            nx.draw_networkx_nodes(self.g, self.pos, ax=subp, nodelist=nodes, node_shape='P', node_size=100)
            self.proxies.append(Line2D(range(1), range(1), marker='P', lw=0))
            self.signs.append('склады')

            nodes = [n.name for n in self.sys.consumers]
            nx.draw_networkx_nodes(self.g, self.pos, ax=subp, nodelist=nodes, node_shape='d', node_size=100)
            self.proxies.append(Line2D(range(1), range(1), marker='d', lw=0))
            self.signs.append('потребители')

        if not node:
            return

        nx.draw_networkx_labels(self.g, self.pos, labels={node.name: node.name}, verticalalignment='center',
                                bbox={'pad': 0.6, 'boxstyle': 'round', 'facecolor': colors['add2']})
        self.proxies.append(Line2D(range(1), range(1), color=colors['add2'], marker='o', lw=0))
        self.signs.append('выбранный пункт')

    def _build_edges(self, subp):
        route = self.config.cur_route

        nx.draw_networkx_edges(self.g, self.pos, ax=subp, width=0.2)
        if not route:
            return
        forward_nodes = [(road.node1, road.node2) for road in route.roads_forward]
        active_edges = [(u.name, v.name) for u, v in forward_nodes]
        nx.draw_networkx_edges(self.g, self.pos, ax=subp, edgelist=active_edges, edge_color=colors['accent3'], width=1,
                               arrowstyle=ArrowStyle('Simple', head_length=1.5, head_width=0.7), arrows=True,
                               arrowsize=15, connectionstyle='arc3,rad=0.1')
        self.proxies.append(Line2D([0, 1], [0, 1], color=colors['accent3'], lw=5))
        self.signs.append('маршрут')

        backward_nodes = [(road.node1, road.node2) for road in route.roads_backward]
        active_edges = [(u.name, v.name) for u, v in backward_nodes]
        nx.draw_networkx_edges(self.g, self.pos, ax=subp, edgelist=active_edges, edge_color=colors['salmon'], width=0.5,
                               arrowstyle=ArrowStyle('Simple', head_length=1.5, head_width=0.7), arrows=True,
                               arrowsize=15, connectionstyle='arc3,rad=0.1')
        self.proxies.append(Line2D([0, 1], [0, 1], color=colors['salmon'], lw=5))
        self.signs.append('обратный маршрут')

    def figure(self) -> plt.Figure:
        plt.close('all')
        self.g = self.graph()
        self.pos = nx.spring_layout(self.g, seed=10)

        fig: plt.Figure = plt.figure()
        subp = fig.add_subplot(111)
        subp.margins(0.2)
        subp.set_position([0, 0, 1, 1])

        self._build_edges(subp)
        self._build_nodes(subp)

        if self.signs and self.proxies:
            plt.legend(self.proxies, self.signs)
        return fig
