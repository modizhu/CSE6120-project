'''This file implements the Approximation Heurestic method to find the minimum vertex cover for a given input graph.

Instructions: The folder structure is as follows: Project Directory contains   [Code,Data,Output].
Language: Python 3
Executable: python Code/Approx.py  -inst Data/karate.graph -alg Approx -time 600 -seed 1045

The seed value will not be used for the Approximation implementaiton.

The output will be two files: *.sol and *.trace created in the project Output folder
*.sol --- record the size of optimum vertex cover and the nodes in it.
*.trace --- record all the optimum solution found 
            during the search and the time it was found
'''
import networkx as nx
import time
import sys
import random
import math
import os
from os import path
import networkx as nx
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

#Check if VC forms vertex cover for G
def isVC(G, VC):
    if VC is None or G is None:
        return False
    for x in G.edges():
        if (x[0] not in VC and x[1] not in VC):
            return False
    return True

def ApproxVC(G, cutoff, trace_file):



# Setup function to initialize graph and run vertex cover and output files
def main(graph_file, output_dir, cutoff, randSeed):
    random.seed(randSeed)
    solution_file = "Output/" + graph_file[5:-6] + "_Approx_" + str(int(cutoff)) + "_" + str(randSeed) + ".sol"
    trace_file = "Output/" + graph_file[5:-6] + "_Approx_" + str(int(cutoff)) + "_" + str(randSeed) + ".trace"
    
    G, N, E = read_graph(graph_file)
    G1 = G.copy()
    
    print("start!")
    deg_sorted, deg_dict = nodesInAscDegree(G)
    sol = ApproxVC(G1, cutoff, trace_file)
    
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