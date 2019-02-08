import entity2vec.node2vec as node2vec
from os import path
import os
import networkx as nx

EDGELIST_DIR = './edgelist'
EMBEDDINGS_DIR = './embeddings'


def main():
    all_query_files = [qf for qf in os.listdir(EDGELIST_DIR) if qf.endswith(".edgelist")]

    G = None

    print('loading edgelists...')
    for query_file in all_query_files:
        print('- ' + query_file)
        H = nx.read_edgelist(path.join(EDGELIST_DIR, query_file), nodetype=str, create_using=nx.DiGraph())
        for edge in H.edges():
            H[edge[0]][edge[1]]['weight'] = 1

        if G is None:
            G = H
        else:
            G = nx.compose(G, H)

    G = G.to_undirected()

    print('Nodes: %d' % nx.number_of_nodes(G))
    print('Edges: %d' % nx.number_of_edges(G))

    n2vOpt = {"directed": False,
              "preprocessing": True,
              "weighted": False,
              "p": 1,
              "q": 1,
              "walk_length": 10,
              "num_walks": 10,
              "dimensions": 100,
              "window_size": 3,
              "workers": 10,
              "iter": 3
              }

    directed = n2vOpt["directed"]
    preprocessing = n2vOpt["preprocessing"]
    weighted = n2vOpt["weighted"]
    p = n2vOpt["p"]
    q = n2vOpt["q"]
    walk_length = n2vOpt["walk_length"]
    num_walks = n2vOpt["num_walks"]
    dimensions = n2vOpt["dimensions"]
    window_size = n2vOpt["window_size"]
    workers = n2vOpt["workers"]
    iter = n2vOpt["iter"]

    print(n2vOpt)

    node2vec_graph = node2vec.Node2Vec(directed, preprocessing, weighted, p, q, walk_length,
                                       num_walks, dimensions, window_size, workers, iter)

    node2vec_graph.G = G

    node2vec_graph.learn_embeddings('%s/%s.emb' % (EMBEDDINGS_DIR, 'midi'), 'text')


if __name__ == '__main__':
    main()
