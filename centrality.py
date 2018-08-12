# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 20:03:04 2018

@author: DELL
"""


"""
Created on Tue Jul 17 11:13:19 2018

@author: Hugo
"""

import networkx as nx
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

G = nx.DiGraph() # create a directed graph called G
#dictionary for yearly centrality
centrality={}
year=['2012','2013','2014','2015','2016']
# Loop reads a csv file with scrap car bilateral trade data

for i in year:
    with open('20122017car.csv', 'r') as csvfile:
        G.clear()
        csv_f = csv.reader(csvfile)
        next(csv_f)
        for row in csv_f:
            if row[0] == i:
                G.add_edge(row[2],row[3],weight=float(row[10]))
    ec = nx.pagerank_numpy(G, weight='weight')
    centrality[i]=ec 
central=pd.DataFrame(data=centrality)
central.to_csv('Pagerankcentrality2012_2016.csv')
# 10 biggest player for plotting
biggestplayer=central.nlargest(10,'2016')

#transpose to have year as index
# page rank value
plt.plot(biggestplayer.transpose())
plt.title('Country centrality 2012-2016')
plt.xlabel('year')
plt.ylabel('Page rank centrality')
plt.legend(biggestplayer.index)
plt.show()
plt.savefig('Page_rank_centrality_20122016.png', dpi=1000)

# pagerank value in basis 2012 (year 2012 = 1)
biggestplayerbase2012=biggestplayer.divide(biggestplayer[:]['2012'].transpose(),axis='index')
plt.plot(biggestplayerbase2012.transpose())
plt.title('Country centrality 2012-2016')
plt.xlabel('year')
plt.ylabel('Page rank centrality, 2012=1')
plt.legend(biggestplayer.index)
plt.show()
plt.savefig('Page_rank_centrality_base2012_20122016.png', dpi=1000)

# pagerank yearly growth

biggestplayergrowth=biggestplayer.transpose().pct_change().transpose().drop('2012',axis=1)
plt.plot(biggestplayergrowth.transpose())
plt.title('Country centrality 2012-2016')
plt.xlabel('year')
plt.ylabel('Page rank centrality growth')
plt.legend(biggestplayer.index)
plt.show()
plt.savefig('Page_rank_centrality_growth.png', dpi=1000)


#Export yearly, trade data pivoted and aggreged by reporter yearly
dataset = pd.read_csv('20122017car.csv').drop('2017',axis=0)
export=dataset.pivot_table(index='ReporterISO3', columns='Year', values='TradeValue in 1000 USD', aggfunc=np.sum,fill_value=0).drop(2017,axis=1)
export.to_csv('totalexport2012_2016.csv')

#
biggestexporter=export.nlargest(10,2016)
plt.plot(biggestexporter.transpose())
plt.title('Country export  2012-2016')
plt.xlabel('year')
plt.ylabel('export ')
plt.legend(biggestexporter.index)
plt.show()
plt.savefig('export_2012-2016.png', dpi=1000)

#export growth
biggestexportergrowth=biggestexporter.transpose().pct_change().transpose().drop(2012,axis=1)
plt.plot(biggestexportergrowth.transpose())
plt.title('Country export growth 2012-2016')
plt.xlabel('year')
plt.ylabel('export growth')
plt.legend(biggestexportergrowth.index)
plt.show()
plt.savefig('export_growth.png', dpi=1000)


