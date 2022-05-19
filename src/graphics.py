import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D
from matplotlib.patches import ArrowStyle

from entities import TransportSystem, Route, GeoNode
from ui.styles import colors


def build_graph(sys: TransportSystem) -> nx.Graph:
    g = nx.Graph()
    for node in sys.nodes:
        g.add_node(node.name)
        for other, road in node.linked.items():
            g.add_edge(node.name, other.name, weight=1 / road.dist, **road.__dict__)

    return g


def get_figure(sys: TransportSystem, route: Route = None, node: GeoNode = None) -> plt.Figure:
    plt.close('all')
    g = build_graph(sys)

    pos = nx.spring_layout(g, seed=10)

    fig: plt.Figure = plt.figure()
    subp = fig.add_subplot(111)
    subp.margins(0.2)
    subp.set_position([0, 0, 1, 1])

    proxies = []
    signs = []

    nx.draw_networkx_edges(g, pos, ax=subp, width=0.2)
    if route:
        forward_nodes = [(road.node1, road.node2) for road in route.roads_forward]
        active_edges = [(u.name, v.name) for u, v in forward_nodes]
        nx.draw_networkx_edges(g, pos, ax=subp, edgelist=active_edges, edge_color=colors['accent3'], width=1,
                               arrowstyle=ArrowStyle('Simple', head_length=2.0, head_width=1.0), arrows=True,
                               arrowsize=20, connectionstyle='arc3,rad=0.1')
        proxies.append(Line2D([0, 1], [0, 1], color=colors['accent3'], lw=5))
        signs.append('маршрут')

        backward_nodes = [(road.node1, road.node2) for road in route.roads_backward]
        active_edges = [(u.name, v.name) for u, v in backward_nodes]
        nx.draw_networkx_edges(g, pos, ax=subp, edgelist=active_edges, edge_color=colors['salmon'], width=0.5,
                               arrowstyle=ArrowStyle('Simple', head_length=2.0, head_width=1.0), arrows=True,
                               arrowsize=20, connectionstyle='arc3,rad=0.1', label='обратный маршрут')
        proxies.append(Line2D([0, 1], [0, 1], color=colors['salmon'], lw=5))
        signs.append('обратный маршрут')

    labels = {n: n for n in g}
    if node:
        del labels[node.name]
        nx.draw_networkx_labels(g, pos, labels={node.name: node.name}, verticalalignment='center',
                                bbox={'pad': 0.6, 'boxstyle': 'round', 'facecolor': colors['add2']})
        proxies.append(Line2D(range(1), range(1), color=colors['add2'], marker='o', lw=0))
        signs.append('выбранный пункт')

    nx.draw_networkx_labels(g, pos, ax=subp, labels=labels, verticalalignment='center',
                            bbox={'pad': 0.4, 'boxstyle': 'round', 'facecolor': colors['accent1']})

    if signs and proxies:
        plt.legend(proxies, signs)
    return fig
