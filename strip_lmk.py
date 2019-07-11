#!/usr/bin/env python
import sys
import webbrowser
import getopt
from geoutils import lmk2csv


def main(argv):
    """
    Strip lmk input file to create a txt outputfile formatted as so:
    number, coord N, coord E,
    """
    lmkfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["lmkfile=", "ofile="])
    except getopt.GetoptError:
        print('strip_lmk.py -i <lmkfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('strip_lmk.py -i <lmkfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--lmkfile"):
            lmkfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    header, rows_data = lmk2csv(open(lmkfile))

    with open(outputfile, 'w+') as f:
        for row in rows_data:
            f.write(row[0].lstrip("0"))
            f.write(",")
            f.write(row[1])
            f.write(",")
            f.write(row[2])
            f.write(",")
            f.write('\n')

    webbrowser.open(outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
