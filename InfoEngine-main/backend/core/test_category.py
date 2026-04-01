
import matplotlib
matplotlib.use("Agg")  # Forces headless mode

import matplotlib.pyplot as plt
import networkx as nx

from backend.core.infoengine_category import I  # your Category instance

def plot_category_graph(category):
    G = nx.DiGraph()

    # nodes
    for obj in category.objects:
        G.add_node(obj)

    # edges
    for (name, dom, cod), m in category.morphisms.items():
        G.add_edge(dom, cod, label=name)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_color="purple", node_size=1500)
    nx.draw_networkx_labels(G, pos, font_color="white", font_size=10)

    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="orange", width=2)

    edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    plt.axis("off")
    plt.tight_layout()
    plt.show()

plt.savefig("category_graph.png")
print("Saved graph to category_graph.png")

if __name__ == "__main__":
    plot_category_graph(I)
