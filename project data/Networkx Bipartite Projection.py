import networkx as nx
from networkx.algorithms import bipartite

B = nx.read_gexf("Style_Release_final.gexf").to_undirected()

top_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)   # releases
bottom_nodes = set(B) - top_nodes                                       # label/style/artist etc.

G = bipartite.weighted_projected_graph(B, top_nodes) #project "1" onto "0", weighted


nx.write_gexf(G, "bipartite_style.gexf")