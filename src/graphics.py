import matplotlib.pyplot as plt
import networkx as nx
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

    nx.draw_networkx_edges(g, pos, ax=subp)
    if route:
        active_edges = [(u.name, v.name) for u, v in zip(route.nodes[:-1], route.nodes[1:])]
        nx.draw_networkx_edges(g, pos, ax=subp, edgelist=active_edges, edge_color=colors['accent3'], width=1,
                               arrowstyle=ArrowStyle('Simple', head_length=2.0, head_width=1.0), arrows=True,
                               arrowsize=20)

    labels = {n: n for n in g}
    if node:
        del labels[node.name]
        nx.draw_networkx_labels(g, pos, labels={node.name: node.name}, verticalalignment='center',
                                bbox={'pad': 0.6, 'boxstyle': 'round', 'facecolor': colors['add2']})
    nx.draw_networkx_labels(g, pos, ax=subp, labels=labels, verticalalignment='center',
                            bbox={'pad': 0.4, 'boxstyle': 'round', 'facecolor': colors['accent1']})
    return fig
