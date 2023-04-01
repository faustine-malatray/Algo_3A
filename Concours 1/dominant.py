import sys
import os
import time
from xml.dom.minicompat import NodeList
import networkx as nx
import random
import matplotlib.pyplot as plt
from networkx import Graph
import numpy as np
from sympy import cycle_length


def node_max_voisinnage(g, D, R):
    nbr_max_voisins = 0
    node_max_voisins = R[0]
    for node in g.nodes:
        if node not in D:
            c = len([neigh for neigh in g.neighbors(node) if neigh in R])
            if c > nbr_max_voisins:
                nbr_max_voisins, node_max_voisins = c, node
            elif c == nbr_max_voisins:
                nbr_max_voisins, node_max_voisins = random.choice(
                    [[nbr_max_voisins, node_max_voisins], [c, node]])
    return [node_max_voisins, nbr_max_voisins]


def del_voisins(g, node, R):
    for neigh in g.neighbors(node):
        if neigh in R:
            R.pop(R.index(neigh))
    return R


def is_cycle(g, R, D):
    try:
        cycle = [(elem[0], elem[1])
                 for elem in nx.find_cycle(g, orientation="ignore")]
        nodes_cycle = set([node for edge in cycle for node in edge])
        if nodes_cycle.issubset(set(R)) and set(R).issubset(nodes_cycle):
            for i in range(len(cycle)):
                if i % 3 == 0:
                    D.append(cycle[i][1])
                    if cycle[i][1] in R:
                        R.pop(R.index(cycle[i][1]))
                    R = del_voisins(g, cycle[i][1], R)
            return [True, D]
        else:
            return [False, None]
    except nx.NetworkXNoCycle:
        return [False, None]


def dominant(g):

    D = []
    R = list(g.nodes)

    while len(R) > 0:
        # traitement des cycles
        bool_cycle, D_cycle = is_cycle(g, R, D)
        if bool_cycle:
            break

        next_node, nbr_voisins = node_max_voisinnage(g, D, R)

        # traitement des noeuds isolés
        if nbr_voisins == 0:
            for node in R:
                D.append(node)
                R.pop(R.index(node))
                R = del_voisins(g, node, R)

        if len(R) == 0:
            break

        D.append(next_node)
        if next_node in R:
            R.pop(R.index(next_node))
        R = del_voisins(g, next_node, R)

    for _ in range(10):
        Dprime = D
        for _ in range(len(D)):
            new = random.choice(Dprime)
            trial = [node for node in D if node != new]
            if nx.is_dominating_set(g, trial):
                Dprime.remove(new)
        D = best(D, Dprime)

    return best(D, D_cycle)


def scoring(D):
    if D == None:
        return np.Inf
    return len(D)


def best(D, Dprime):
    if scoring(D) <= scoring(Dprime):
        return D
    else:
        return Dprime

    #########################################
    #### Ne pas modifier le code suivant ####
    #########################################
if __name__ == "__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])

    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(input_dir, "doesn't exist")
        exit()

    # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(
        time.strftime("%d%b%Y_%H%M%S", time.localtime()))
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    score_tot = 0

    for graph_filename in sorted(os.listdir(input_dir)):
        # importer le graphe
        g = nx.read_adjlist(os.path.join(input_dir, graph_filename))

        # calcul du dominant
        D = sorted(dominant(g), key=lambda x: int(x))

        # ajout au rapport
        output_file.write(graph_filename)
        for node in D:
            output_file.write(' {}'.format(node))
        output_file.write('\n')

    output_file.close()
