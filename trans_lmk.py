#!/usr/bin/env python
import sys
import webbrowser
import getopt
from geoutils import trans_coordinates, lmk2csv


def main(argv):
    """
    Translate of give delta_x and delta_y the 2D coordinates of lmk input file.
    Return an updated lmk file as outputfile.
    """
    lmkfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:x:y:o:", ["lmkfile=", "ofile="])
    except getopt.GetoptError:
        print('trans_lmk.py -i <lmkfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('trans_lmk.py -i <lmkfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--lmkfile"):
            lmkfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    header, rows_data = lmk2csv(open(lmkfile))

    delta_x = input("Inserisci delta x: ")
    delta_y = input("Inserisci delta y: ")

    trans_rows = trans_coordinates(delta_x, delta_y, rows_data)

    with open(outputfile, 'w+') as file:
        file.write('\n'.join(header))
        file.write('\n')
        for row in trans_rows:
            file.write(row[0])
            file.write(str(row[1]).rjust(10))
            file.write(str(row[2]).rjust(10))
            file.write(str(row[3]).rjust(5))
            file.write(str(row[4]).rjust(8))
            file.write(str(row[5]).rjust(9))
            file.write(str(row[6]).rjust(7))
            file.write(str(row[7]).rjust(7))
            file.write(str(row[8]).rjust(7))
            file.write('\n')

    webbrowser.open(outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
