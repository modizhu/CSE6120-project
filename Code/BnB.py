'''This file implements the Branch and Bound method to find minimum vertex cover for a given input graph.

Instructions: The folder structure is as follows: Project Directory contains   [Code,Data,Output]. The code files must be pasted in Code folder.

Language: Python 3
Executable: python Code/BnB.py -inst Data/karate.graph -alg BnB -time 600 -seed 100 
The seed value will not be used for the BnB implementaiton.

The output will be two files: *.sol and *.trace created in the project Output folder
*.sol --- record the size of optimum vertex cover and the nodes in it.
*.trace --- record all the optimum solution found 
            during the search and the time it was found
'''

from collections import defaultdict
import time, math, sys

class RunBnB:
    # Get graph from .graph file
    def get_graph(self, name):
        data = open(name)
        data = data.readlines()

        overview = data[0].split()

        graph = defaultdict(set)
        graphset = []
        for i in range(1, len(data)):
            sub = data[i].split()
            for j in range(len(sub)):
                graph[i].add(int(sub[j]))
                if (i, int(sub[j])) not in graphset:
                    graphset.append((int(sub[j]), i))
        return graph, graphset

    def find_maxdegree(self, G):
        node_good_list = sorted(G.items(), key = lambda x: len(x[1]), reverse = True)
        return node_good_list
        
    def LB(self, G_p, degree):
        if not G_p:
            return 0
        lb = math.ceil(len(G_p.keys())/ degree)
        return lb

    def find_V_p(self, graph, C_p):#C_p can be viewed as selected nodeset
        V_p = set()
        related_to_C_p = set()

        for node in C_p:
            related_to_C_p.add(node)

        for node in graph.keys():
            if node not in related_to_C_p:
                V_p.add(node)
        #     print(V_p)
        return V_p

    def find_E_p(self, graph, V_p):
        E_p = set()
        for node in V_p:
            u = node
            for v in graph[u]:
                if u in V_p and v in V_p and (v, u) not in E_p:
                    E_p.add((u, v))
    #     print(E_p)
        return E_p

    def form_graph(self, E):#Form corresponding graph based on given V and E
        graph = defaultdict(set)
        
        for edge in E:
            graph[edge[0]].add(edge[1])
            graph[edge[1]].add(edge[0])
        return graph

    def branch_and_bound(self, graph, max_time):
        start_time = time.time()
        # max_time = 600;      # This is the maximum time that we run the branch and bound algorithm
        
        vertex_list = graph.keys()
        vertex_No = len(vertex_list)
        
        # We need to notice that upperbound is the worst case, and lowerbound is the possible best case
        
        upperbound = vertex_No       #The worst case is that every node is selected
        
        possible_stack = []
        checked = set()
        
        #We start from nothing
        C_p = []
        V_p = self.find_V_p(graph, C_p)
        E_p = self.find_E_p(graph, V_p)
        G_p = self.form_graph(E_p)
    #     lowerbound = find_lowerbound(C_p, G_p)
        lowerbound = 1  
        possible_stack.append((C_p, lowerbound, checked))
        
    # sort the possible solutions, and we will look at the one that has highest lb
        possible_stack.sort(key = lambda x:-x[1])
        curr_time = time.time() - start_time
        lowest_lowerbound = upperbound
        while possible_stack and curr_time < max_time:
    #         print(time.time(), 'Begin', possible_stack)
        
            curr = possible_stack.pop()
            curr_set = curr[0]
            curr_checked = curr[2]

    #         print(time.time(), 'POP', curr)

            V_p = self.find_V_p(graph, curr[0])
            E_p = self.find_E_p(graph, V_p)
            G_p = self.form_graph(E_p)
    #         print(G_p, 'G_p')
            if not G_p:# That means every edge has been covered, we get an answer
                return end_time - start_time, curr_set, len(curr_set)
            


            node_good_list = self.find_maxdegree(G_p)
            if not node_good_list:
                continue
            
    #         print(curr_checked, 'curr_checked')
    #         print(node_good_list, 'node_good_list')
            
            selected = 0
            for (node, links) in node_good_list:
                if node not in curr_checked:
                    # print(node, links)
                    next_degree = len(links)
                    next_node = node
                    selected = 1
                    break
            
            if not selected:
                continue
                
    #         print(next_node, 'next_node')
            new_checked = curr_checked.copy()
            new_checked.add(next_node)
            
            #If not add this next_node, we just add the next_node to checked set
            possible_stack.append((curr_set, curr[1], new_checked))
            
            #If add this next_node
            C_p = curr[0] + [next_node]
            V_p = self.find_V_p(graph, C_p)
            E_p = self.find_E_p(graph, V_p)
            G_p = self.form_graph(E_p)
            
            lb = self.LB(G_p, next_degree)
            lowerbound = len(C_p) + lb
            upperbound = min(upperbound, len(C_p) + len(G_p.keys()))#The worst case is that we need to select all the nodes left
    #         print(C_p, lowerbound, upperbound)
            # if lowerbound > upperbound:Not good, prune the corresponding one, no continue
            if lowerbound <= upperbound:
                possible_stack.append((C_p, lowerbound, new_checked))

    #         possible_stack.sort(key = lambda x:-x[1])
        
            end_time = time.time()
            curr_time = end_time - start_time
                
            if curr_time > max_time:
                print('Has reached maximum time')
                return end_time - start_time, curr_set, len(curr_set)
                
        print('Has reached bottom') 
        return end_time - start_time, curr_set, len(curr_set)


    def main(self):
        num_args = len(sys.argv)
        # print(sys.argv)
        # print(num_args)

        if num_args == 5:
           graph_file = sys.argv[1]
           algo_name = sys.argv[2]
           max_time = int(sys.argv[3])
        
        # Construct graph
        if algo_name == 'BnB':
            graph, graphset = self.get_graph(graph_file)
        
        

        t, mvc, lenmvc = self.branch_and_bound(graph, max_time)

        output_file = graph_file[:-6] + '_BnB_' + str(max_time) + '.sol'
        output = open(output_file, 'w')
        output.write(str(lenmvc) + "\n")
        output.write(str(mvc) + "\n")
        output.write('time = ' + str(t))

        # Only one valid solution will be found by BnB
        outtrace_file = graph_file[:-6] + '_BnB_' + str(max_time) + '.trace'
        outtrace = open(outtrace_file, 'w')
        outtrace.write(str(t) + ', ' + str(lenmvc))


if __name__ == '__main__':
    # run the experiments
    runexp = RunBnB()
    runexp.main()

