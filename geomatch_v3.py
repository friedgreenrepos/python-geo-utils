#!/usr/bin/python
import webbrowser
import sys
import getopt
import csv
from itertools import combinations
from math import hypot


def rows2list(open_file):
    """Return a list of the input file's rows."""
    points = []
    with open_file as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            points.append((row[0], row[1], row[2]))
    return points


def point2D_dist(a, b):
    """
    Return distance between 2-dimensional points a,b.

    Points are tuple/array of point id, X coordinate, Y coordinate.
    i.e:
    a = (IDa, Xa, Ya)
    b = (IDb, Xb, Yb)
    """
    return hypot(int(b[1]) - int(a[1]), int(b[2]) - int(a[2]))


def comb2dist_list(comb_list):
    """Return the list of distances given a 2D points tuple list."""
    dist_list = []
    for comb in comb_list:
        dist_list.append(point2D_dist(comb[0], comb[1]))
    return dist_list


def comb2dist_dict_list(comb_list):
    """
    Return a list of dictionaries from a list of 2D points.

    Dictionaries will have the following keys:
    - first point 2D-coordinates,
    - second point 2D-coordinates
    - the distance between them.
    """
    dist_dict_list = []
    for comb in comb_list:
        dist_dict_list.append({
                'point_a': comb[0],
                'point_b': comb[1],
                'dist_ab': point2D_dist(comb[0], comb[1]),
                }
        )
    return dist_dict_list


def comb2dist_tuple_list(comb_list):
    """
    Return a list of tuple from a list of 2D points.

    Elements of each tuple will be the following:
    - first point 2D coordinates,
    - second point 2D coordinates
    - the distance between them.
    """
    dist_tuple_list = []
    for comb in comb_list:
        dist_tuple_list.append(
            (comb[0], comb[1], point2D_dist(comb[0], comb[1]))
        )
    return dist_tuple_list


def get_dup_list(dist_tuple_list):
    """Return a list of points couples with the same distance list."""
    dup_list = []
    sorted_by_dist = sorted(dist_tuple_list, key=lambda tup: tup[2])
    i = 0
    while i < (len(sorted_by_dist)-1):
        sub_list = []
        while (sorted_by_dist[i+1][2] - sorted_by_dist[i][2] < 0.5):
            sub_list.append(sorted_by_dist[i])
            sub_list.append(sorted_by_dist[i+1])
            i += 1
        if sub_list:
            sub_list = list(set(sub_list))
            dup_list.append(sub_list)
        i += 1
    return dup_list


def main(argv):
    """
    Return a list of same-distance points couples from a file of 2D points.

    Given a csv file (inputfile) will:
    - Create a list of tuple (IDp, Xp, Yp)
    - Create a list of all possible combinations of these points
    - Create a list of these combinations points distances.
    - Search for any matching distances between these combinations.
    """
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('geomatch.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('geomatch.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    points = rows2list(open(inputfile))

    comb_list = list(combinations(points, 2))

    dist_tuple_list = comb2dist_tuple_list(comb_list)

    dup_list = get_dup_list(dist_tuple_list)

    with open(outputfile, "w+") as f:
        for dup in dup_list:
            f.write("Match!\n#{} ({}, {}) and #{} ({}, {}), dist={:06.3f}\n#{} ({}, {}) and #{} ({}, {}), dist={:06.3f}\n"\
                    .format(dup[0][0][0], dup[0][0][1], dup[0][0][2], dup[0][1][0],
                            dup[0][1][1], dup[0][1][2], dup[0][2], dup[1][0][0],
                            dup[1][0][1], dup[1][0][2], dup[1][1][0], dup[1][1][1],
                            dup[1][1][2], dup[1][2],)
            )

    webbrowser.open(outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
