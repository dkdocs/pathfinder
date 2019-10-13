#!/usr/bin/env python

from pathfinder import seek
import csv
from math import ceil
from pprint import PrettyPrinter
import numpy as np

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

cell_width = 2000 # In pixels

n_rows = ceil((boundaries['bottom'] - boundaries['top']) / cell_width) + 1
n_columns = ceil((boundaries['right'] - boundaries['left']) / cell_width) + 1

grid = [[0] * n_columns for i in range(n_rows)]

for point in points:
    x, y = point
    col = int((x - boundaries['left']) / cell_width)
    row = int((y - boundaries['top']) / cell_width)
    grid[row][col] = 1

origins = np.asarray(grid)

if __name__ == "__main__":    
    path_finder_results = seek(
        origins,
        targets=None,
        weights=None,
        path_handling='link',
        debug=False,
        film=False
    )

    pp.pprint(path_finder_results)
