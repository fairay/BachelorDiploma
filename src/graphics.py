import matplotlib.pyplot as plt
import networkx as nx

from entities import TransportSystem


def build_graph(sys: TransportSystem) -> nx.Graph:
    G = nx.Graph()
    for node in sys.nodes:
        G.add_node(node, name=node.name)
        for other, vals in node.linked.items():
            G.add_edge(node, other, weight=1 / vals['dist'], **vals)

    return G


def get_figure(sys: TransportSystem) -> plt.Figure:
    G = build_graph(sys)
    pos = nx.spring_layout(G, scale=1.0)

    fig: plt.Figure = plt.figure()
    subp = fig.add_subplot(111)
    subp.margins(0.2)
    subp.set_position([0, 0, 1, 1])

    nx.draw_networkx_nodes(G, pos, ax=subp)
    nx.draw_networkx_edges(G, pos, ax=subp)
    nx.draw_networkx_labels(G, pos, ax=subp, verticalalignment='center', bbox=dict(alpha=1, pad=0.5, boxstyle='round'))
    return fig
