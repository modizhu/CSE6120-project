'''This file implements the Local Search - hill climbing to find the minimum vertex cover for a given input graph.

Instructions: The folder structure is as follows: Project Directory contains [Code,Data,Output]. 

Language: Python 3
Executable: python Code/ls1.py  -inst Data/karate.graph -alg ls1 -time 600 -seed 1045

The seed value will be used for the Local Search implementaiton.

The output will be two files: *.sol and *.trace created in the project Output folder
*.sol --- record the size of optimum vertex cover and the nodes in it.
*.trace --- record all the optimum solution found 
            during the search and the time it was found


This local search implementation iteratively takes an initial solution, removes a node and again iteratively swaps 
            till the solution is a vertex cover again. Performance has been improved by implementing taboo methods (conf_check).             
'''

import networkx as nx
import time
import sys
import random
import math
import os
from os import path
import networkx as nx
from networkx.algorithms.approximation import vertex_cover
import time
import sys
import random
from os import listdir
from os.path import isfile, join
import argparse



# Read in file to networkx graph structure
def read_graph(filename):
    with open(filename, 'r') as f:
        file = f.readlines()
    for line_num, line in enumerate(file):
        graph_data = list(map(lambda x: int(x), line.split()))
        if line_num==0:
            N = graph_data[0] # Number of Vertices
            E = graph_data[1] # Number of Edges
            G = nx.Graph()    # Graph object
        else:
            for adj_nodes in graph_data:
                G.add_edge(line_num, adj_nodes)
    return G,N,E

# Forming queue with nodes arranged in ascending order of degree
# We will iterate over this queue/list  by deleting the node and checking VC validity
def nodesInAscDegree(G):
    degrees_sorted = list(set(dict(G.degree()).values())) # set of unique degress of nodes in graph

    # {degree: [node1,node2,..]}; dict with 'degree' as key and 'nodes having that degree' as value
    deg_nodes_dict = {}
    for deg in degrees_sorted:
        deg_nodes_dict[deg] = []
    for node,deg in list(dict(G.degree()).items()):
        deg_nodes_dict[deg].append(node)
    deg_nodes_dict
    return degrees_sorted, deg_nodes_dict

#Check if VC forms vertex cover for G
def isVC(G, VC):
    if VC is None or G is None:
        return False
    for x in G.edges():
        if (x[0] not in VC and x[1] not in VC):
            return False
    return True

#hill climbing algorithm
def hillClimbing(G, degrees_sorted, deg_nodes_dict, cutoff, trace_file):
    VC = G.copy()
    len_deg_sorted = len(degrees_sorted)
    deg_ptr = 0
    _trace = []
    start_time=time.time()
    while(deg_ptr<len_deg_sorted and ((time.time()-start_time)<cutoff)):  
        deg = degrees_sorted[deg_ptr]
        random.shuffle(deg_nodes_dict[deg]) #randomly shuffle nodes with same degree
        for node in deg_nodes_dict[deg]:
            node_edges = list(VC.edges(node)) # Saving node's edges before deleting the node to add it back if not VC
            VC.remove_node(node)
            if isVC(G,VC):
                _trace.append([time.time()-start_time, VC.number_of_nodes()])
                continue
            else:
                VC.add_edges_from(node_edges) # adding back the node to VC
        deg_ptr+=1
    
    # Writing the .trace file
    with open(trace_file, 'w') as f:
        for t,n in _trace:
            f.write(str(t) + ', ' + str(n) + '\n') 
    return VC



# Setup function to initialize graph and run vertex cover and output files
def main(graph_file, output_dir, cutoff, randSeed):
    random.seed(randSeed)
    solution_file = "Output/" + graph_file[5:-6] + "_LS1_" + str(int(cutoff)) + "_" + str(randSeed) + ".sol"
    trace_file = "Output/" + graph_file[5:-6] + "_LS1_" + str(int(cutoff)) + "_" + str(randSeed) + ".trace"
    
    G, N, E = read_graph(graph_file)
    G1 = G.copy()
    
    print("start!")
    deg_sorted, deg_dict = nodesInAscDegree(G)
    sol = hillClimbing(G1, deg_sorted, deg_dict, cutoff, trace_file)
    
    nodes = sorted(list(sol.nodes()))
    node_size = len(list(sol.nodes()))
    with open(solution_file,'w') as f:
        f.write(str(node_size) + '\n')
        for n in nodes:
            f.write(str(n) + ',')
    print("Completed!")
            
    
if __name__ == '__main__':
    graph_file = sys.argv[1]
    cutoff = int(sys.argv[2])
    output_dir = ''
    randSeed = sys.argv[3]
    main(graph_file, output_dir, cutoff, randSeed)
