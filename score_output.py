from utils import read_file, write_file, Graph, score_partitioning, random_partition, partition_count
import numpy as np
import datetime
from crawl_utils import *
import pickle
import os
import difflib

# Input prompt for filename
DIRs = [x for x in os.listdir("outputs/")]
i = 0
for DIR in DIRs:
    print(i, DIR)
    i += 1

output_num = int(input("Output number:"))
output_name = DIRs[output_num]
filename_output = "outputs/" + output_name

# Input prompt for filename
DIRs = [x for x in os.listdir("data/")]
i = 0
for DIR in DIRs:
    print(i, DIR)
    i += 1

data_num = int(input("Output number:"))
data_name = DIRs[data_num]

graph, _ = read_file(data_name)

partitioning = []
with open(filename_output, "r") as f:
    for line in f.readlines():
        if line[0] == "#" or line[0] == " ":
            continue

        line = line.split(" ")
        partitioning.append(int(line[1]))

print("Score:", score_partitioning(graph, partitioning))



