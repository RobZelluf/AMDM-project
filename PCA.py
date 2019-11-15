from utils import *

import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering


def embedding(graph, d):
    pca = PCA(n_components=d)
    vec = pca.fit_transform(graph.laplacian)

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


# Agglomerative Hierarchical Clustering
ac = AgglomerativeClustering(5)
ac.fit(embeddings)
ac_labels = ac.labels_
for i in range(5):
    print("Num", i, " - ", len([x for x in ac_labels if x == i]))
score = score_partitioning(graph, ac_labels)
print(score)


# CONFIRMING SC OUTPUT

# counter = 0
# for n in range(len(graph.vertices)):
#     for m in range(len(graph.vertices)):
#         if sc_labels[n] != sc_labels[m]:
#             if graph.adjacency_matrix[n,m] == 1:
#                 print("WRONG")
#             else:
#                 counter += 1
# print(counter)


# Make similar sized clusters
#
# new_labels = np.zeros(len(labels))
# distances = np.zeros(5)
# for i in range(len(labels)):
#     for k in range(5):
#         distances[k] = np.linalg.norm(embeddings[i] - k_means.cluster_centers_[k])
#     new_cluster = np.where(min(distances))[0][0]
#     new_labels[i] = np.where(min(distances))[0][0]
