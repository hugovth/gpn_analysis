
"""
Created on Tue Jul 17 11:13:19 2018
adapted from and strongly inspired by https://briandew.wordpress.com/2016/06/15/trade-network-analysis-why-centrality-matters/
@author: Hugo
"""

import networkx as nx
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import itertools
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from networkx.algorithms import community
from random import random
from networkx import edge_betweenness_centrality 

G = nx.DiGraph() # create a directed graph called G
 
# Loop reads a csv file with scrap car bilateral trade data
with open('20122017car.csv', 'r') as csvfile:
    csv_f = csv.reader(csvfile)
    next(csv_f)
    for row in csv_f:
        if row[0] == "2017":
            G.add_edge(row[2],row[3],weight=float(row[10]))
#usachnexp = G['USA']['CHN']['weight']
#print ('USA 2012 vehicule exports to China, in USD: ' + str(usachnexp))
            
            
# Calculate eigenvector centrality of matrix G 
# with the exports value as weights

# Blank dictionary to store total exports of each country
totexp = {}

# Calculate total exports of each country in the network
for exp in G.nodes():
    tx=0
    for elem in [g for exp,f,g in G.out_edges(exp, data=True)]:
     for key, value in elem.items():
         tx+= value
    totexp[exp] = tx
number=[totexp[key] for key in totexp]
avgexp = np.mean(number) 
number=[totexp[key] for key in totexp]
avgexp = np.mean(number) 
nx.set_node_attributes(G,totexp, name='totexp')
#Cleaning the graph

#remove node and edge that are irrelevant,
#we took country representing 0.05 % of word export an edge coresponding 5% of export of each country
 
wordexp=G.size(weight='weight')
minwordexp=wordexp/2000
removenode=[]
for exp in G.nodes():
    if G.nodes[exp]['totexp']< minwordexp:
        removenode.append(exp)
removeedge=[]
for (u, v) in G.out_edges():  
    if G[u][v]['weight']<G.nodes[u]['totexp']*0.05:
        removeedge.append((u,v))
G.remove_edges_from(removeedge)
G.remove_nodes_from(removenode)
nx.info(G)
# Calculate eigenvector/page rank centrality of matrix G 
#change formula for different type of centrality
# with the exports value as weights
ec = nx.pagerank_numpy(G, weight='weight')

# Set centrality as a node attribute for each node
nx.set_node_attributes(G,ec, name='cent')
node_color = [float(G.node[v]['cent']) for v in G]




# Use the results later for the node's size in the graph, expended 10 time for visualisation
node_size = [float(G.nodes[v]['totexp'])*10 / avgexp for v in G]
#edge_size = [G[u][v]['weight'] / avgexp for u,v in G]
edge_size = [G[u][v]['weight']/ avgexp for (u,v) in G.edges()]

# Visualization 
# Calculate position of each node in G using networkx spring layout
pos = nx.spring_layout(G,k=30,iterations=8) 

# Draw nodes
nodes = nx.draw_networkx_nodes(G,pos, node_size=node_size, node_color=node_color, alpha=0.4) 
# Draw edges
edges = nx.draw_networkx_edges(G, pos, edge_color='lightgray', arrows=True, arrowsize=5, width=edge_size, alpha=0.4)

# Add labels
nx.draw_networkx_labels(G,pos,font_size=5)
nodes.set_edgecolor('gray')

# Add labels and title
plt.text(-0.75,-1.1, 'Node color is eigenvector centrality; Node size is value of global exports', fontsize=7)
plt.title('Scrap car trade network, 2017', fontsize=12)

# Bar with color scale for eigenvalues
cbar = plt.colorbar(mappable=nodes, cax=None, ax=None, fraction=0.015, pad=0.04)
cbar.set_clim(0, 1)

# Plot options
plt.margins(0,0)
plt.axis('off')

# Save as high quality png
plt.savefig('760200.png', dpi=1000)

#clustering using newman  
def most_central_edge(G):
    centrality =nx.edge_betweenness_centrality(G, weight='weight')
    max_cent = max(centrality.values())
    centrality = {e: c / max_cent for e, c in centrality.items()}
    return max(centrality, key=centrality.get)
comp = community.girvan_newman(G,most_valuable_edge=most_central_edge)

#for communities in itertools.islice(comp, 5):
#    print(tuple(sorted(c) for c in communities))
#tuple(sorted(c) for c in next(comp))
i = 1
while i<4:
    cluster=tuple(sorted(c) for c in next(comp))
    i += 1
print(cluster)
#for cluster in cluster:
#    nx.subgraph(G,cluster)
    

#for subgraph in nx.strongly_connected_components(G):
for cluster in cluster:
    H=G.subgraph(cluster)
    if H.number_of_nodes()>2:
        print(nx.eigenvector_centrality_numpy(H, weight='weight'))
