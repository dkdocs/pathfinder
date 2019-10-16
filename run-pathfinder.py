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
from simplekml import Kml
# from osgeo import gdal, osr

kml = Kml()

points = []
rows = None

with open('new_towers_combined.csv') as f:
    reader = csv.DictReader(f)
    rows = [row for row in reader]

ZOOM_SCALE = 500000

points = [(int((float(row['longitude']) + 90) * ZOOM_SCALE), int((float(row['latitude']) + 90) * ZOOM_SCALE)) for row in rows]
coordinates = [(float(row['latitude']), float(row['longitude'])) for row in rows]



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

reference = (
    min(map(lambda location: location[0], coordinates)),
    min(map(lambda location: location[1], coordinates)),
    max(map(lambda location: location[0], coordinates)),
    max(map(lambda location: location[1], coordinates))
)

cell_width = 300 # In pixels

n_rows = ceil((boundaries['bottom'] - boundaries['top']) / cell_width) + 1
n_columns = ceil((boundaries['right'] - boundaries['left']) / cell_width) + 1

scale = (
    (reference[2] - reference[0]) / n_rows,
    (reference[3] - reference[1]) / n_columns
)

grid = [[0] * int(n_columns) for i in range(int(n_rows))]
targets = [[0] * int(n_columns) for i in range(int(n_rows))]

point_to_grid_map = {}

for idx, point in enumerate(points):
    x, y = point
    col = int((x - boundaries['left']) / cell_width)
    row = int((y - boundaries['top']) / cell_width)
    targets[row][col] = 1
    if (idx % 1000) == 0:
        grid[row][col] = 1

    point_to_grid_map[(row, col)] = idx
    

origins = np.asarray(grid)
targets = np.asarray(targets)

pp.pprint(targets)
pp.pprint(origins)

# gdalAccess = gdal
# ds = gdal.Open()
# crs = osr.SpatialReference()
# crs.ImportFromWkt(ds.GetProjectionRef())
# create lat/long crs with WGS84 datum
# crsGeo = osr.SpatialReference()
# crsGeo.ImportFromEPSG(4326)  # 4326 is the EPSG id of lat/long crs
# transformer = osr.CoordinateTransformation(crs, crsGeo)

def point_to_latlong(point):
    if point in point_to_grid_map:
        row = rows[point_to_grid_map[point]]
        return (row['longitude'], row['latitude'])
    else:
        y = point[0]
        x = point[1]

        lt = reference[0] + y * scale[0]
        lg = reference[1] + x * scale[1]

        return (lg, lt)

def convert_pixel_latlong(points):
    return (
        point_to_latlong(points[0]),
        point_to_latlong(points[1])
    )
    
def is_equal_point(point1, point2):
    return point1[0] == point2[0] and point1[1] == point2[1]

def find_path_pixel(path_matrix):
    for i, row in enumerate(path_matrix):
        for j, cell in enumerate(row):
            if cell > 0:
                return (i, j)

def get_path_neighbors(cell, path_matrix):
    neighbors = []
    for diff_x in [-1, 0, 1]:
        for diff_y in [-1, 0, 1]:
            loc = (cell[0] + diff_x, cell[1] + diff_y)
            if not (diff_x == 0 and diff_y == 0) and cell[0] + diff_x > 0 and cell[1] + diff_y > 0 and path_matrix[loc] == 1:
                neighbors.append(loc)
    return neighbors

def graph_walker(current_cell, tower_to_connect, path_matrix, edges: list, level=0):
    if level > 2000:
        return
    # print('level=%d' % level)
    if current_cell is None:
        return

    path_matrix[current_cell] = 0
    if tower_to_connect is None:
        tower_to_connect = current_cell

    for neighbor in get_path_neighbors(current_cell, path_matrix):
        if neighbor in point_to_grid_map:
            edges.append((tower_to_connect, neighbor))
        next_to_connect = neighbor if neighbor in point_to_grid_map else tower_to_connect
        graph_walker(neighbor, next_to_connect, path_matrix, edges, level + 1)


if __name__ == "__main__":    
    path_finder_results = seek(
        origins,
        point_to_grid_map,
        targets=targets,
        weights=None,
        path_handlings='link',
        debug=False,
        film=False
    )
    paths = path_finder_results['paths']
    # Save paths pixels to png image
    imsave('output.png', paths)

    # edges = path_finder_results['edges']

    all_edges = []

    current_cell = find_path_pixel(paths)
    while not current_cell is None:
        graph_walker(current_cell, None, paths, all_edges)
        current_cell = find_path_pixel(paths)
    
    coordinates_for_line = convert_pixel_latlong(all_edges[0])
    pp.pprint(all_edges)
    line_count = 0
    max_path_length = 0
    # for i in range(1, len(all_edges)):
    #     edge = all_edges[i]
    #     if is_equal_point(all_edges[i-1][1], all_edges[i][0]):
    #         coordinates_for_line.append(point_to_latlong(all_edges[i][1]))
    #     else:
    #         kml.newlinestring(name='Transmisssion Line %d' % line_count, description='', coords=coordinates_for_line)
    #         max_path_length = max(max_path_length, len(coordinates_for_line))
    #         line_count += 1
    #         coordinates_for_line = convert_pixel_latlong(edge)
    for idx, edge in enumerate(all_edges):
        coordinates_for_line = convert_pixel_latlong(edge)
        kml.newlinestring(name='Transmisssion Line %d' % idx, description='', coords=coordinates_for_line)
        max_path_length = max(max_path_length, len(coordinates_for_line))
        line_count += 1
        coordinates_for_line = convert_pixel_latlong(edge)
    # kml.newlinestring(name='Transmisssion Line %d' % line_count, description='', coords=coordinates_for_line)
    max_path_length = max(max_path_length, len(coordinates_for_line))

    pp.pprint(kml)
    paths_save_file_path = 'paths_%d.kml' % cell_width
    kml.save(paths_save_file_path, format=True)
    pp.pprint('paths_save_file_path: %s' % paths_save_file_path)
    pp.pprint('max_path_length: %d' % max_path_length)
    pp.pprint('line_count: %d' % line_count)
    # Save paths pixels to png image
    imsave('output-after.png', paths)

