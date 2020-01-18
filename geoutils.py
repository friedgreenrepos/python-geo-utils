import csv
import xmltodict
import copy
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


def fill_xml_points(points, xml_path):
    """
    Update an xml file with points passed as argument.

    The xml file is parsed as a dictionary and then the X, Y coordinates values
    of every 'Riflettore' are updated with the points' coordinates.
    """
    dict = {}
    # That b in the mode specifier in the open() states that the file shall be treated as binary.
    # So dict will remain a bytes. No decoding attempt will happen this way.
    with open(xml_path, 'rb') as fd:
        dict = xmltodict.parse(fd.read())
        count = 0
        for rif in dict['Impianto']['Riflettori']['Riflettore']:
            if rif['@Numero'] == points[count][0]:
                rif['Y'] = points[count][2]
                rif['X'] = points[count][1]
            count += 1
    return dict


def lmk2csv(open_lmk):
    """
    Create a csv file from a lmk one.
    Return header lines as an array, column titles as a string
    and remaining rows as array of arrays.
    """
    lines = [line.rstrip('\n') for line in open_lmk]
    header = []
    # pop header lines out of file (lines that start with # + 1)
    line_count = 0
    for line in lines:
        if line[0] == '#':
            header.append(line)
            line_count += 1
        else:
            header.append(line)
            line_count += 1
            break
    for i in range(0, line_count):
        lines.pop(0)
    # strip spaces to get an array of elements
    rows_data = []
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

        rows_data.append(csv_array)
    return header, rows_data


def match_el_array(el, rows, index=0):
    """
    Search for matches of 'el' in 'rows' of given 'index'.
    Return row of first found match or empty array.
    """
    for row in rows:
        if el == row[index]:
            return row
    return []


def swap_csv_coordinates(swapfile, rows):
    """
    Replace coordinates in rows with ones read from swapfile.
    - copy swapfile into array of array
    - check if original row has to be replaced
      (pad swapfile 0-th element with zeroes to compare correctly)
    - if so write a new row with swapfile values otherwise write original row
    Return array of final swapped rows as arrays.
    """
    swap_rows = []
    with open(swapfile) as swap_csv:
        swap_reader = csv.reader(swap_csv, delimiter=',')
        for swap_row in swap_reader:
            swap_new = list(swap_row)
            r_0 = str(swap_row[0]).zfill(6)
            swap_new[0] = r_0
            swap_rows.append(swap_new)
    swapped_rows = []
    for row in rows:
        tmp_row = match_el_array(row[0], swap_rows)
        if tmp_row:
            swapped_row = [
                row[0],
                tmp_row[1],
                tmp_row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
            ]
            swapped_rows.append(swapped_row)
        else:
            swapped_rows.append(row)
    return swapped_rows


def convert_to_point(n):
    '''Convert input number to int from exponential notation '''
    if 'D' in str(n):
        n = n.split("D")
        n_exp = int(n[1])
        if n_exp > -4:
            n_base = float(n[0])
            n = n_base * 10 ** n_exp
        else:
            n = float(0)
    return n


def trans_coordinates(delta_x, delta_y, rows_data):
    '''Translate 2D coordinates using delta_x and delta_y'''
    trans_rows = copy.deepcopy(rows_data)
    for t_row in trans_rows:
        t_row[1] = int(t_row[1]) + int(delta_x)
        t_row[2] = int(t_row[2]) + int(delta_y)
    return trans_rows
