#!/usr/bin/python

import networkx
import pygraphviz

G = networkx.Graph()
G.add_node(0)
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_edge(0, 1)
G.add_edge(0, 2)
G.add_edge(1, 2)
G.add_edge(2, 3)
A = networkx.nx_agraph.to_agraph(G)
A.node_attr['style'] = 'filled'
A.node_attr['width'] = '0.4'
A.node_attr['height'] = '0.4'
A.edge_attr['color'] = '#000000'
A.get_node(0).attr['fillcolor'] = '#FF0000'
A.get_node(1).attr['fillcolor'] = '#0000FF'
A.get_node(2).attr['fillcolor'] = '#00FF00'
A.get_node(3).attr['fillcolor'] = '#FF0000'
A.layout()
A.draw("out.png", format = 'png')