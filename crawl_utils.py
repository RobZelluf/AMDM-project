from utils import Graph, read_file, score_partitioning
import numpy as np


def one_crawl(graph, v, steps):
    vertices_reached = list()
    for i in range(steps):
        v = graph.get_connected_vertex(v)
        vertices_reached.append(v)
    return vertices_reached


def select_init(graph, seed=0, blacklist=[]):
    visit_count = [0] * graph.num_vertices
    for i in range(10000):
        vertices = one_crawl(graph, seed, 20)
        for v in vertices:
            visit_count[v] += 1
    max_visit = max(t for t in visit_count if visit_count.index(t) not in blacklist)
    init_vert = visit_count.index(max_visit)
    return init_vert


def grow_monster_partition(graph, seed=0, size=1000, blacklist=None):
    # if blacklist = None:
    #     blacklist = list()
    partition = list()
    init_vert = seed
    partition.append(init_vert)
    visit_count = [0] * graph.num_vertices

    for p in range(size - 1):
        if p % int(size / 10) == 0:
            print("Assigning vertex ", p, "out of", size, "- ",
                  int(p / size * 100), "%")
            total_visits = sum(visit_count)
            in_visits = sum([visit_count[i] for i in partition])
            out_visits = total_visits - in_visits
            print("Visit count in partition: ", int(in_visits / len(partition)))
            print("Visit count outside partition: ", int(out_visits / (graph.num_vertices - len(partition))))

        for c in range(1000):
            vertices = one_crawl(graph, init_vert, 3)
            for v in vertices:
                visit_count[v] += 1
            # print("Visit Variance: ", np.var(visit_count))
        m = max(t for t in visit_count if visit_count.index(t) not in (partition + blacklist))
        init_vert = visit_count.index(m)
        partition.append(init_vert)
    return partition, visit_count.index(min(visit_count))


#
#
def init_partitions(graph, num_partitions, init_size=10, seed=0):
    total_visit_count = [0] * graph.num_vertices
    init_partitions = list()
    blacklist = list()
    for k in range(num_partitions):
        init_vert = select_init(graph, seed, blacklist)
        print("Initializing partition ", k)
        partition_visit_count = [0] * graph.num_vertices
        partition_verts = list()
        partition_verts.append(init_vert)
        init_partitions.append(partition_verts)
        for j in range(init_size):
            for i in range(1000):
                verts = one_crawl(graph, init_vert, 3)
                for v in verts:
                    partition_visit_count[v] += 1

            # What a hack!
            blacklist = [item for sublist in init_partitions for item in sublist]
            m = max(t for t in partition_visit_count if partition_visit_count.index(t) not in blacklist)
            init_vert = partition_visit_count.index(m)
            print(init_vert)
            partition_verts.append(init_vert)
            init_partitions.pop()
            init_partitions.append(partition_verts)
        total_visit_count = [sum(x) for x in zip(partition_visit_count, total_visit_count)]
        seed = total_visit_count.index(min(total_visit_count))
    return init_partitions


def assign_partition(graph, partitioning, normalization, assign_v, num_partitions, threshold=0):
    visit_count = np.zeros(graph.num_vertices)
    crawls = 300 - int((sum(normalization) / graph.num_vertices) * 200)
    steps = 3 - int((sum(normalization) / graph.num_vertices) * 2)
    if assign_v % int(graph.num_vertices / 100) == 0:
        print("Assigning partition ", assign_v, "out of", graph.num_vertices, "- ",
              int(assign_v / graph.num_vertices * 100), "%")
        print("Crawls: ", crawls)
        print("Steps: ", steps)
        print("Partition sizes: ", normalization)
    for i in range(crawls):
        verts = one_crawl(graph, assign_v, steps)
        for v in verts:
            visit_count[v] += 1
    # Which partition?
    votes = np.zeros(num_partitions)
    for i in range(len(visit_count)):
        if partitioning[i] != -1:
            votes[partitioning[i]] += visit_count[i]
    if assign_v % int(graph.num_vertices / 100) == 0:
        print(votes)
    normalized_votes = np.divide(votes, normalization)
    normalized_votes = normalized_votes / (sum(normalized_votes) + 0.001)
    votes_sorted = normalized_votes.copy()
    votes_sorted.sort()
    if votes_sorted[-1] - votes_sorted[-2] >= threshold:
        return normalized_votes.argmax()
    else:
        return -1
