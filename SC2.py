from utils import *
from sklearn.cluster import KMeans
from scipy.sparse.linalg import eigsh

graph, num_partitions = read_file()
laplacian = graph.laplacian

vals, vecs = eigsh(graph.laplacian)

vecs = vecs[:, np.argsort(vals)]
vals = vals[np.argsort(vals)]

# kmeans on first three vectors with nonzero eigenvalues
kmeans = KMeans(n_clusters=num_partitions)
kmeans.fit(vecs[:, 1:20])

labels = kmeans.labels_
for i in range(num_partitions):
    print("Num", i, " - ", len([x for x in labels if x == i]))

score = score_partitioning(graph, labels)
print("Score:", score)