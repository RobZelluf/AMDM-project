from utils import read_file, Graph, score_partitioning

import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def embedding(graph, d):
    pca = PCA(n_components=d)
    vec = pca.fit_transform(graph.adjacency_matrix)

    return vec


graph = read_file()
embeddings = embedding(graph, 100)

k_means = KMeans(5)
k_means.fit(embeddings)
labels = k_means.labels_
for i in range(5):
    print("Num", i, " - ", len([x for x in labels if x == i]))

score = score_partitioning(graph, labels)
print(score)

