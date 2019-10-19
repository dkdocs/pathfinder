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
from functools import reduce
from sklearn.cluster import DBSCAN
from geopy.distance import vincenty as distance
import json
import os
import sys

# distance.vincenty((-22.867461, -43.5026573), (-22.8668212, -43.4972522))
# from osgeo import gdal, osr

kml = Kml()

points = []
rows = None

with open('new_towers_combined.csv') as f:
    reader = csv.DictReader(f)
    rows = [row for row in reader]

# Constants
ZOOM_SCALE = 500000
cell_width = 100 # In pixels
iMaxStackSize = 8000

points = [(int((float(row['longitude']) + 90) * ZOOM_SCALE), int((float(row['latitude']) + 90) * ZOOM_SCALE)) for row in rows]
coordinates = [(float(row['latitude']), float(row['longitude'])) for row in rows]



# json.dump([{ 'label': 'Tower %d' % (idx + 1), 'location': coordinate } for idx, coordinate in enumerate(coordinates)], open('coordinates.json', 'w'))

# Create cluster oof points
def distance_in_m(p1, p2):
    return distance(p1, p2).m
# coordinate_cluster_output = DBSCAN(eps=70, min_samples=1, metric=distance_in_m, n_jobs=-1).fit(coordinates)
coordinate_cluster_output = {
    'labels_': [0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 32, 34, 35, 34, 35, 36, 36, 37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 52, 53, 54, 55, 56, 57, 58, 58, 57, 56, 55, 54, 53, 59, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 105, 106, 107, 106, 108, 109, 110, 109, 110, 111, 109, 110, 111, 111, 112, 113, 114, 112, 113, 114, 112, 113, 114, 115, 116, 115, 116, 115, 116, 117, 118, 117, 118, 117, 119, 120, 121, 122, 119, 121, 122, 119, 120, 121, 122, 120, 122, 123, 123, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 133, 134, 135, 136, 137, 138, 139, 140, 141, 134, 135, 136, 137, 138, 139, 140, 142, 142, 141, 134, 135, 136, 137, 138, 139, 140, 143, 141, 134, 144, 141, 134, 143, 141, 134, 124, 145, 127, 124, 145, 127, 128, 129, 128, 146, 129, 146, 147, 148, 130, 148, 130, 149, 148, 149, 150, 150, 151, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 154, 162, 165, 166, 167, 158, 168, 169, 170, 170, 171, 162, 167, 172, 173, 160, 174, 168, 175, 163, 155, 172, 176, 162, 157, 153, 167, 160, 163, 161, 165, 166, 154, 166, 152, 177, 169, 174, 175, 164, 165, 177, 171, 170, 162, 178, 158, 176, 156, 153, 179, 178, 156, 179, 155, 173, 180, 179, 152, 176, 174, 177, 181, 182, 183, 184, 185, 186, 187, 186, 188, 189, 190, 189, 191, 192, 193, 192, 185, 190, 182, 194, 127, 195, 196, 196, 197, 198, 187, 186, 195, 199, 200, 201, 184, 198, 202, 203, 199, 204, 205, 206, 194, 207, 205, 204, 208, 209, 201, 193, 183, 159, 186, 210, 211, 212, 213, 214, 214, 215, 216, 214, 217, 218, 219, 220, 221, 213, 216, 222, 219, 220, 222, 223, 224, 217, 211, 225, 218, 215, 226, 223, 227, 224, 224, 228, 212, 212, 215, 217, 211, 220, 213, 219, 223, 210, 229, 229, 230, 231, 230, 232, 233, 234, 235, 232, 232, 236, 229, 237, 238, 233, 239, 230, 240, 235, 236, 241, 240, 237, 239, 230, 238, 235, 240, 242, 240, 232, 229, 232, 235, 229, 236, 240, 243, 235, 234, 239, 237, 235, 239, 234, 230, 241, 229, 231, 233, 230, 239, 242, 243, 240, 237, 242, 237, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 251, 255, 256, 257, 258, 259, 260, 259, 261, 262, 263, 253, 264, 265, 266, 267, 268, 267, 269, 270, 271, 272, 273, 272, 274, 273, 245, 275, 276, 270, 249, 277, 249, 278, 265, 268, 258, 279, 265, 280, 281, 282, 283, 284, 285, 286, 287, 286, 288, 289, 290, 291, 289, 274, 292, 293, 294, 295, 296, 295, 297, 248, 298, 299, 300, 264, 280, 296, 260, 301, 246, 262, 291, 281, 293, 254, 292, 296, 255, 278, 252, 276, 251, 284, 299, 289, 287, 293, 261, 299, 302, 247, 303, 269, 303, 256, 294, 263, 298, 304, 305, 286, 271, 272, 303, 285, 306, 305, 307, 282, 270, 302, 308, 250, 309, 259, 291, 266, 300, 245, 310, 277, 257, 309, 290, 307, 311, 283, 301, 256, 275, 302, 288, 304, 312, 312, 313, 314, 314, 315, 313, 316, 317, 318, 319, 319, 317, 314, 319, 315, 320, 312, 320, 321, 320, 313, 322, 323, 322, 318, 315, 321, 321, 323, 317, 323, 324, 325, 325, 324, 325, 324, 326, 326, 326, 327, 328, 329, 330, 331, 332, 332, 333, 334, 333, 333, 329, 332, 334, 331, 335, 335, 329, 335, 328, 331, 330, 329, 332, 332, 332, 328, 330, 334, 336, 337, 336, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 341, 353, 354, 355, 356, 357, 358, 339, 359, 222, 360, 361, 362, 363, 364, 365, 351, 353, 366, 360, 349, 366, 341, 344, 367, 368, 369, 370, 371, 340, 350, 360, 366, 372, 356, 373, 368, 340, 359, 345, 358, 374, 368, 346, 358, 375, 363, 376, 375, 377, 376, 378, 356, 379, 375, 354, 352, 359, 359, 367, 372, 346, 352, 380, 353, 377, 345, 339, 381, 339, 354, 344, 382, 377, 350, 379, 383, 363, 384, 378, 378, 385, 386, 387, 388, 389, 390, 391, 390, 392, 393, 394, 393, 395, 396, 386, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 389, 408, 401, 393, 409, 396, 392, 395, 402, 410, 400, 411, 385, 387, 409, 399, 408, 411, 394, 391, 404, 409, 399, 408, 410, 397, 412, 398, 389, 393, 385, 413, 400, 406, 403, 386, 398, 402, 401, 394, 414, 395, 404, 414, 391, 415, 406, 393, 415, 392, 414, 389, 412, 388, 393, 396, 390, 416, 388, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 445, 441, 446, 447, 448, 448, 449, 450, 427, 451, 452, 453, 438, 429, 454, 455, 454, 456, 457, 437, 442, 458, 422, 456, 459, 444, 421, 460, 461, 462, 463, 435, 464, 458, 420, 465, 466, 467, 426, 468, 466, 469, 470, 469, 467, 471, 472, 439, 471, 428, 472, 457, 447, 473, 474, 475, 476, 436, 477, 478, 446, 479, 461, 480, 430, 481, 482, 483, 484, 470, 449, 477, 459, 485, 485, 450, 419, 486, 487, 478, 480, 433, 462, 488, 465, 468, 489, 432, 490, 451, 418, 488, 452, 425, 460, 453, 491, 476, 490, 489, 492, 463, 493, 494, 495, 496, 497, 493, 498, 498, 80, 499, 500, 501, 499, 500, 502, 503, 504, 505, 503, 505, 494, 497, 504, 80, 506, 507, 508, 124, 509, 510, 511, 512, 513, 514, 515, 512, 516, 517, 518, 519, 511, 520, 521, 522, 519, 523, 524, 525, 524, 526, 527, 528, 529, 507, 530, 531, 532, 533, 534, 535, 536, 537, 538, 178, 530, 539, 540, 541, 542, 542, 397, 403, 543, 544, 271, 545, 546, 210, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 573, 575, 576, 575, 577, 555, 578, 579, 580, 581, 582, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 590, 592, 593, 594, 595, 596, 597, 589, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 595, 610, 611, 598, 612, 613, 614, 551, 615, 616, 617, 618, 619, 620, 599, 574, 621, 622, 577, 553, 623, 624, 625, 584, 626, 625, 555, 605, 627, 628, 622, 608, 615, 603, 623, 616, 629, 557, 552, 550, 606, 594, 596, 621, 611, 586, 592, 578, 561, 580, 607, 562, 576, 602, 563, 604, 560, 568, 566, 620, 570, 559, 579, 581, 626, 630, 572, 629, 587, 610, 614, 613, 591, 600, 565, 631, 632, 585, 633, 609, 618, 567, 624, 612, 601, 634, 635, 558, 564, 583, 633, 619, 571, 548, 629, 627, 617, 597, 555, 593, 556, 559, 636, 549, 637, 569, 638, 633, 639, 640, 640, 641, 554, 641, 640, 642, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 645, 659, 648, 648, 660, 661, 658, 651, 658, 662, 651, 663, 643, 664, 665, 649, 652, 666, 661, 667, 647, 650, 666, 647, 657, 650, 664, 668, 669, 670, 668, 671, 670, 672, 673, 651, 651, 667, 674, 675, 676, 677, 649, 662, 666, 678, 657, 679, 642, 645, 646, 659, 659, 652, 680, 664, 676, 661, 663, 651, 681, 682, 683, 684, 685, 682, 685, 686, 683, 686, 684, 687, 688, 689, 690, 691, 692, 693, 694, 695, 694, 692, 689, 696, 697, 689, 698, 688, 699, 700, 697, 701, 696, 688, 702, 696, 703, 704, 687, 705, 706, 697, 707, 693, 692, 687, 708, 692, 709, 710, 711, 692, 238, 231, 712, 713, 714, 714, 714, 715, 713, 716, 716, 717, 718, 719, 720, 721, 721, 719, 722, 720, 723, 724, 262, 725, 359, 726, 727, 728, 729, 730, 339, 731, 732, 733, 734, 735, 736, 737, 738, 739, 20, 740, 740, 511, 741, 524, 742, 526, 743, 510, 744, 745, 746, 747, 745, 519, 748, 749, 519, 750, 751, 748, 522, 751, 505, 503, 494, 752, 497, 500, 753, 754, 755, 756, 757, 758, 759, 760, 502, 761, 762, 763, 764, 765, 177, 766, 767, 768, 282, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 792, 793, 793, 794, 795, 796, 795, 794, 795, 796, 797, 797, 798, 799, 800, 799, 801, 800, 799, 802, 803, 804, 803, 804, 802, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 291, 358, 228, 228, 835, 836, 837, 838, 839, 840, 841, 842, 843, 838, 844, 845, 846, 847, 848, 849, 850, 848, 851, 852, 843, 853, 854, 846, 855, 856, 857, 858, 842, 847, 859, 860, 861, 862, 863, 864, 856, 851, 840, 865, 837, 836, 866, 855, 867, 867, 866, 868, 869, 870, 869, 870, 868, 871, 872, 873, 872, 874, 874, 871, 875, 876, 877, 878, 116, 879, 880, 880, 881, 882, 882, 883, 884, 885, 117, 886, 886, 886, 886, 887, 888, 171, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 905, 905, 906, 906, 906, 907, 907, 908, 909, 910, 141, 599, 551, 144, 142, 911, 911, 142, 143, 912, 913, 914, 915, 916, 917, 895, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 927, 928, 929, 930, 797, 931, 932, 932, 932, 933, 933, 934, 934, 934, 931, 931, 935, 936, 937, 938, 938, 939, 940, 941, 685, 942, 681, 943, 944, 658, 649, 650, 652, 945, 946, 947, 948, 949, 950, 951, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 655, 964, 650, 965, 966, 705, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 993, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1009, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 818, 1037, 818, 1038, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1048, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1056, 142, 808, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 711, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 890, 216, 1075, 1075, 1075, 1075, 1075, 886, 1076, 1076, 1076, 1076, 1077, 1077, 262, 262, 262, 225, 225, 1078, 1078, 1078, 1079, 1079, 1079, 216, 1080, 1080, 1080, 1081, 1081, 227, 227, 1082, 1082, 1082, 218, 221, 221, 297, 306, 1083, 1084, 1085, 1085, 1081, 118, 733, 1086, 1087, 1088, 1089, 1090, 221, 221, 221, 221, 226, 216, 1091, 1091, 1091, 372, 1092, 339, 339, 359, 359, 226, 193, 193, 193, 116, 117, 1093, 1093, 1094, 1095, 202, 927, 1096, 1096, 555, 555, 559, 559, 1097, 1098, 1099, 1100, 1101, 1102, 1102, 1102, 1102, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1108, 1109, 1109, 1110, 1111, 1112, 1113, 1114, 1102, 1102, 1102, 1101, 1100, 1099, 1098, 1097, 559, 559, 663, 1115, 663, 646, 1116, 659, 659, 659, 659, 659, 659, 1115, 1117, 1117, 1117, 1118, 1118, 1118, 1119, 1120, 1120, 1121, 1122, 1122, 1122, 1123, 1124, 1124, 1124, 1125, 1126, 1126, 1126, 1127, 1127, 1128, 1129, 1117, 1117, 1117, 1117, 1130, 1131, 502, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1135, 1140, 1137, 1141, 1134, 1139, 1133, 1142, 1143, 1144, 1142, 1143, 1133, 1145, 1146, 1147, 1148, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1153, 1155, 1156, 1157, 1158, 1159, 1160, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1156, 1157, 1160, 1158, 1173, 1174, 1175, 1176, 1177, 1178, 1133, 1133, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1205, 1205, 165, 165, 1206, 1207, 1207, 1208, 1208, 1208, 1209, 1210, 275, 303, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 1247, 1248, 1224, 1225, 1226, 1227, 1249, 1229, 1231, 1232, 1233, 1250, 1234, 1235, 1236, 1251, 1237, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1252, 1244, 1245, 1247, 1248, 1253, 1254, 1255, 1256, 402, 262, 262, 262, 262, 270, 270, 270, 270, 270, 410, 282, 282, 285, 795, 1257, 1257, 1257, 1257, 1257, 1258, 1258, 1259, 1260, 1261, 1261, 1261, 1261, 1261, 1262, 1263, 1264, 1265, 1266, 1267, 1268, 667, 667, 1269, 1270, 1271, 1272, 1273, 1274, 1275, 835, 1276, 1277, 1278, 859, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1287, 1288, 1289, 63, 1290, 1291, 1292]
}


pp = PrettyPrinter(indent=4, width= 250)

number_of_clusters = max(coordinate_cluster_output['labels_']) + 1

cluster = np.full(number_of_clusters, {
        'center': (0, 0),
        'points': []
    })

for idx, point in enumerate(coordinates):
    label = coordinate_cluster_output['labels_'][idx]
    current_points = cluster[label]['points'] + [point]

    center = tuple(sum(map(np.array, current_points)) / len(current_points))

    cluster[label] = {
        'center': center,
        'points': current_points
    }

cluster_coordinates = np.array(list(map(lambda c: (np.array(c['center']) + 90) * ZOOM_SCALE, cluster)))

cluster_points = cluster_coordinates // cell_width

# print(points)
X = np.array(list(map(lambda point: point[0], cluster_points)))
Y = np.array(list(map(lambda point: point[1], cluster_points)))

# Top, Right, Botttom, Left
boundaries = {
    'top': min(Y),
    'right': max(X),
    'bottom': max(Y),
    'left': min(X)
}

reference = (
    min(map(lambda location: location[0], cluster_coordinates)),
    min(map(lambda location: location[1], cluster_coordinates)),
    max(map(lambda location: location[0], cluster_coordinates)),
    max(map(lambda location: location[1], cluster_coordinates))
)

n_rows = ceil(boundaries['bottom'] - boundaries['top']) + 1
n_columns = ceil(boundaries['right'] - boundaries['left']) + 1

scale = (
    (reference[2] - reference[0]) / n_rows,
    (reference[3] - reference[1]) / n_columns
)

grid = np.full((n_columns, n_rows), 0)
targets = np.full((n_columns, n_rows), 0)

point_to_grid_map = {}

for idx, point in enumerate(cluster_points):
    x, y = point
    row = int(y - boundaries['top'])
    col = n_columns - int(x - boundaries['left']) - 1
    targets[(col, row)] = 1
    # print((col, row))
    if (idx % 1000) == 0:
        grid[(col, row)] = 1

    if (col, row) in point_to_grid_map:
        point_to_grid_map[(col, row)].append(idx)
    else:
        point_to_grid_map[(col, row)] = [idx]

origins = grid

imsave('targets.png', targets)
imsave('origins.png', origins)

def point_to_latlong(point):
    if point in point_to_grid_map:
        num_towers = len(point_to_grid_map[point])
        coordinates_sum = list(map(float, \
            reduce(lambda x, y: (float(x[0]) + float(y[0]), float(x[1]) + float(y[1])), \
                map(\
                    lambda tower: (cluster[tower]['center'][1], cluster[tower]['center'][0]), \
                    point_to_grid_map[point]) \
            ) \
        ))
        return (coordinates_sum[1] * 1.0 / num_towers, coordinates_sum[0] * 1.0 / num_towers)
    else:
        y = point[0]
        x = point[1]

        lt = reference[0] + y * scale[0]
        lg = reference[1] + x * scale[1]

        return (lt, lg)

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
    max_y, max_x = path_matrix.shape
    X = [-1, 0, 1]
    Y = [-1, 0, 1]
    if cell[0] == 0:
        Y = Y[1:]
    if cell[0] == path_matrix.shape[0]-1:
        Y = Y[:-1]
    if cell[1] == 0:
        X = X[1:]
    if cell[1] == path_matrix.shape[1]-1:
        X = X[:-1]

    for diff_x in X:
        for diff_y in Y:
            loc = (cell[0] + diff_y, cell[1] + diff_x)
            if not (diff_x == 0 and diff_y == 0) and path_matrix[loc] == 1:
                neighbors.append(loc)
    return neighbors

def save_edges_to_kml(edges):
    line_count = 0
    max_path_length = 0

    coordinates_for_line = convert_pixel_latlong(all_edges[0])
    for idx, edge in enumerate(edges):
        coordinates_for_line = convert_pixel_latlong(edge)
        coordinates_for_line = tuple(map(lambda row: (row[1], row[0]), coordinates_for_line))
        kml.newlinestring(name='Transmisssion Line %d' % idx, description='', coords=coordinates_for_line)
        max_path_length = max(max_path_length, len(coordinates_for_line))
        line_count += 1
        coordinates_for_line = convert_pixel_latlong(edge)
    # kml.newlinestring(name='Transmisssion Line %d' % line_count, description='', coords=coordinates_for_line)
    max_path_length = max(max_path_length, len(coordinates_for_line))

    pp.pprint(kml)
    paths_save_file_path = 'paths_v2_%d.kml' % cell_width
    kml.save(paths_save_file_path, format=True)
    pp.pprint('paths_save_file_path: %s' % os.path.realpath(paths_save_file_path))
    pp.pprint('max_path_length: %d' % max_path_length)
    pp.pprint('line_count: %d' % line_count)


def graph_walker(current_cell, tower_to_connect, path_matrix, edges: list, level=0):
    # print('level=%d' % level)
    # if level > 2000:
    #     print('level=%d' % level)
    #     return level
    if current_cell is None:
        return level

    path_matrix[current_cell] = 0
    if tower_to_connect is None:
        tower_to_connect = current_cell

    for neighbor in get_path_neighbors(current_cell, path_matrix):
        if neighbor in point_to_grid_map:
            edges.append((tower_to_connect, neighbor))
        next_to_connect = neighbor if neighbor in point_to_grid_map else tower_to_connect
        level = max(level, graph_walker(neighbor, next_to_connect, path_matrix, edges, level + 1))

    return level

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
    # Save paths pixels to png image
    imsave('output_v2.png', paths)

    # edges = path_finder_results['edges']

    all_edges = []

    current_cell = find_path_pixel(paths)
    current_stack_size = sys.getrecursionlimit()
    sys.setrecursionlimit(iMaxStackSize)
    while not current_cell is None:
        max_level = graph_walker(current_cell, None, paths, all_edges)
        print('max_level', max_level)
        current_cell = find_path_pixel(paths)
    sys.setrecursionlimit(current_stack_size)
    # pp.pprint(all_edges)
    # for i in range(1, len(all_edges)):
    #     edge = all_edges[i]
    #     if is_equal_point(all_edges[i-1][1], all_edges[i][0]):
    #         coordinates_for_line.append(point_to_latlong(all_edges[i][1]))
    #     else:
    #         kml.newlinestring(name='Transmisssion Line %d' % line_count, description='', coords=coordinates_for_line)
    #         max_path_length = max(max_path_length, len(coordinates_for_line))
    #         line_count += 1
    #         coordinates_for_line = convert_pixel_latlong(edge)

    save_edges_to_kml(all_edges)

    # Save paths pixels to png image
    imsave('output-after_v2.png', paths)

