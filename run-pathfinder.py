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
from osgeo import gdal, osr

kml = Kml()

points = []


with open('towers_combined.csv') as f:
    reader = csv.DictReader(f)
    points = [(int(row['X_img']), int(row['Y_img'])) for row in reader]

with open('towers_combined.csv') as f:
    reader = csv.DictReader(f)
    coordinates = [(float(row['latitude']), float(row['longitude'])) for row in reader]

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

cell_width = 200 # In pixels

n_rows = ceil((boundaries['bottom'] - boundaries['top']) / cell_width) + 1
n_columns = ceil((boundaries['right'] - boundaries['left']) / cell_width) + 1

scale = (
    (reference[2] - reference[0]) / n_rows,
    (reference[3] - reference[1]) / n_columns
)

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

gdalAccess = gdal
# ds = gdal.Open()
# crs = osr.SpatialReference()
# crs.ImportFromWkt(ds.GetProjectionRef())
# create lat/long crs with WGS84 datum
# crsGeo = osr.SpatialReference()
# crsGeo.ImportFromEPSG(4326)  # 4326 is the EPSG id of lat/long crs
# transformer = osr.CoordinateTransformation(crs, crsGeo)

def point_to_latlong(point):
    y = point[0]
    x = point[1]

    lt = reference[0] + (n_rows - y) * scale[0]
    lg = reference[1] + x * scale[1]

    return (lg, lt)

def convert_pixel_latlong(points):
    
    return [
        point_to_latlong(points[0]),
        point_to_latlong(points[1])
    ]
    
def is_equal_point(point1, point2):
    return point1[0] == point2[0] and point1[1] == point2[1]

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

    edges = path_finder_results['edges']

    coordinates_for_line = convert_pixel_latlong(edges[0])
    # pp.pprint(edges)
    line_count = 0
    for i in range(1, len(edges)):
        edge = edges[i]
        if is_equal_point(edges[i-1][1], edges[i][0]):
            coordinates_for_line.append(point_to_latlong(edges[i][1]))
        else:
            kml.newlinestring(name='Transmisssion Line %d' % line_count, description='', coords=coordinates_for_line)
            line_count += 1
            coordinates_for_line = convert_pixel_latlong(edge)
    
    kml.newlinestring(name='Transmisssion Line %d' % line_count, description='', coords=coordinates_for_line)

    pp.pprint(kml)
    kml.save('paths.kml', format=True)
    # Save paths pixels to png image
    # imsave('output.png', paths)

