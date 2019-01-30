import webbrowser
import sys
import getopt
import csv
from itertools import combinations
from geoutils import(rows2list, comb2dist_tuple_list, get_dup_list)


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
        print('match_distance.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('match_distance.py -i <inputfile> -o <outputfile>')
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
