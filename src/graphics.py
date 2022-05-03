import matplotlib.pyplot as plt
import networkx as nx

from entities import TransportSystem


def build_graph(sys: TransportSystem) -> nx.Graph:
    g = nx.Graph()
    for node in sys.nodes:
        g.add_node(node.name)
        for other, road in node.linked.items():
            g.add_edge(node.name, other.name, weight=1 / road.dist, **road.__dict__)

    return g


def get_figure(sys: TransportSystem) -> plt.Figure:
    g = build_graph(sys)
    pos = nx.spring_layout(g, scale=1.0, seed=10)

    fig: plt.Figure = plt.figure()
    subp = fig.add_subplot(111)
    subp.margins(0.2)
    subp.set_position([0, 0, 1, 1])

    # nx.draw_networkx_nodes(G, pos, ax=subp)
    nx.draw_networkx_edges(g, pos, ax=subp)
    nx.draw_networkx_labels(g, pos, ax=subp, verticalalignment='center', bbox=dict(alpha=1, pad=0.5, boxstyle='round'))
    return fig
