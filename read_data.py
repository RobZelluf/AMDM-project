import numpy as np
import pandas as pd
import pickle
from utils import read_file, Graph

filename = 'roadNet-CA.txt'

graph = read_file()

print(graph.get_connected_vertex(50))




