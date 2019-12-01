import numpy as np
import pandas as pd
import pickle
from utils import read_file, create_nx_graph
import networkx as nx

filename = 'roadNet-CA.txt'

graph = create_nx_graph(filename)

nx.draw(graph)




