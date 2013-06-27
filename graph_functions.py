import networkx as nx
import numpy as np

def within_module_degree(graph, partition):
    '''
    Computes the within-module degree for each node.

    ------
    Inputs
    ------

    graph = sparse networkx graph
    partition = modularity partition of graph

    ------
    Output
    ------
    
    wd_dict: Dictionary of the within-module degree of each node.

    '''
    wd_dict = {}
    paths = nx.shortest_path_length(G=graph)
    for m in partition.keys():
        mod_list = partition[m]
        mod_wd_dict = {}
        for source in mod_list:
            count = 0
            for target in mod_list:
                if paths[source][target] == 1:
                    count += 1
            mod_wd_dict[source] = count
        all_mod_wd = mod_wd_dict.values()
        avg_mod_wd = float(all_mod_wd.sum()) / len(all_mod_wd)
        for source in mod_list:
            wd_dict[source] = (mod_wd_dict[source] - avg_mod_wd) / np.std(all_mod_wd)
    return wd_dict

def participation_coefficient(graph, partition):
    '''
    Computes the participation coefficient for each node.

    ------
    Inputs
    ------

    graph = sparse networkx graph
    partition = modularity partition of graph

    ------
    Output
    ------
    
    List of the participation coefficient for each node.

    '''
    
    pc_dict = {}
    all_nodes = set(graph.nodes())
    paths = nx.shortest_path_length(G=graph)
    for m in partition.keys():
        mod_list = set(partition[m])
        between_mod_list = list(set.difference(all_nodes, mod_list))
        for source in mod_list:
            degree = float(nx.degree(G=graph, nbunch=source))
            count = 0
            for target in between_mod_list:
                if paths[source][target] == 1:
                    count += 1
            bm_degree = count
            pc = 1 - (bm_degree / degree)**2
            pc_dict[source] = pc
    return pc_dict

