from utils import *
from sklearn.cluster import KMeans

graph = read_file()

laplacian = graph.laplacian

vals, vecs = np.linalg.eig(laplacian)

vecs = vecs[:,np.argsort(vals)]
vals = vals[np.argsort(vals)]

k_means = KMeans(5)

k_means.fit(vecs)
labels = k_means.labels_
for i in range(5):
    print("Num", i, " - ", len([x for x in labels if x == i]))

score = score_partitioning(graph, labels)
print(score)