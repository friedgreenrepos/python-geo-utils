import csv
import xmltodict
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
        })
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
    while i < (len(sorted_by_dist) - 1):
        sub_list = []
        while (sorted_by_dist[i + 1][2] - sorted_by_dist[i][2] < 0.5):
            sub_list.append(sorted_by_dist[i])
            sub_list.append(sorted_by_dist[i + 1])
            i += 1
        if sub_list:
            sub_list = list(set(sub_list))
            dup_list.append(sub_list)
        i += 1
    return dup_list


def fill_xml_points(points, open_xml):
    """
    Update an xml file with points passed as argument.

    The xml file is parsed as a dictionary and then the X, Y coordinates values
    of every 'Riflettore' are updated with the points' coordinates.
    """
    dict = {}
    with open_xml as fd:
        dict = xmltodict.parse(fd.read())
        count = 0
        for rif in dict['Impianto']['Riflettori']['Riflettore']:
            if rif['@Numero'] == points[count][0]:
                rif['Y'] = points[count][2]
                rif['X'] = points[count][1]
            count += 1
    return dict


def lmk2csv(open_lmk, outputfile):
    """
    Create a csv file from a lmk one.
    Return header lines as an array and write csv file into 'outputfile'.
    """
    lines = [line.rstrip('\n') for line in open_lmk]
    header = []
    # pop header lines out of file
    for i in range(0, 14):
        ln = lines.pop(0)
        header.append(ln)
    # strip spaces to get an array of elements
    final_array = []
    for ln in lines:
        csv_array = []
        csv_array.append(ln[0:6])
        csv_array.append(ln[7:16].replace(" ", ""))
        csv_array.append(ln[17:26].replace(" ", ""))
        csv_array.append(ln[27:31].replace(" ", ""))
        csv_array.append(ln[32:39].replace(" ", ""))
        csv_array.append(ln[40:48].replace(" ", ""))

        if ln[49:55].replace(" ", ""):
            csv_array.append(ln[49:55].replace(" ", ""))
        else:
            csv_array.append(0)
        if ln[56:62].replace(" ", ""):
            csv_array.append(ln[56:62].replace(" ", ""))
        else:
            csv_array.append(0)
        if ln[63:69].replace(" ", ""):
            csv_array.append(ln[63:69].replace(" ", ""))
        else:
            csv_array.append(0)

        final_array.append(csv_array)
    # write array to csv
    with open(outputfile, 'w+') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerows(final_array)
    return header
