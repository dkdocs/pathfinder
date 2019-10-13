#!/usr/bin/env python

from pathfinder import seek
import csv
from math import ceil
from pprint import PrettyPrinter
import numpy as np
from random import randint
import ipdb
from shapely.geometry import Point, LineString
from skimage.io import imsave

points = []


with open('/Users/manishsharma/Downloads/towers_combined.csv') as f:
    reader = csv.DictReader(f)
    points = [(int(row['X_img']), int(row['Y_img'])) for row in reader]

pp = PrettyPrinter(indent=4, width= 250)

# print(points)
X = list(map(lambda point: point[0], points))
Y = list(map(lambda point: point[1], points))

# Top, Right, Botttom, Left
boundaries = {
    'top': min(Y),
    'right': max(X),
    'bottom': max(Y),
    'left': min(X)
}

cell_width = 200 # In pixels

n_rows = ceil((boundaries['bottom'] - boundaries['top']) / cell_width) + 1
n_columns = ceil((boundaries['right'] - boundaries['left']) / cell_width) + 1

grid = [[0] * int(n_columns) for i in range(int(n_rows))]
targets = [[0] * int(n_columns) for i in range(int(n_rows))]

for idx, point in enumerate(points):
    x, y = point
    col = int((x - boundaries['left']) / cell_width)
    row = int((y - boundaries['top']) / cell_width)
    targets[row][col] = 1
    if (idx % 1000) == 0:
        grid[row][col] = 1

origins = np.asarray(grid)
targets = np.asarray(targets)

pp.pprint(targets)
pp.pprint(origins)

if __name__ == "__main__":    
    path_finder_results = seek(
        origins,
        targets=targets,
        weights=None,
        path_handlings='link',
        debug=False,
        film=False
    )
    paths = path_finder_results['paths']


