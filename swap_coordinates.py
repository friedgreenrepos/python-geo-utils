#!/usr/bin/env python
import sys
import webbrowser
import getopt
from geoutils import swap_csv_coordinates, lmk2csv


def main(argv):
    """
    Replace x, y coordinates of lmk input file with new ones read in csv input
    file.
    Return a lmk updated file as outputfile.
    """
    lmkfile = ''
    swapfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:s:o:", ["lmkfile=", "swapfile=", "ofile="])
    except getopt.GetoptError:
        print('swap_coordinates.py -i <lmkfile> -s <swapfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('swap_coordinates.py -i <lmkfile> -s <swapfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--lmkfile"):
            lmkfile = arg
        elif opt in ("-s", "--swapfile"):
            swapfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    header, rows_data = lmk2csv(open(lmkfile))

    swapped_rows = swap_csv_coordinates(swapfile, rows_data)

    with open(outputfile, 'w+') as f:
        f.write('\n'.join(header))
        f.write('\n')
        for fr in swapped_rows:
            f.write(fr[0])
            f.write(str(fr[1]).rjust(10))
            f.write(str(fr[2]).rjust(10))
            f.write(str(fr[3]).rjust(5))
            f.write(str(fr[4]).rjust(8))
            f.write(str(fr[5]).rjust(9))
            f.write(str(fr[6]).rjust(7))
            f.write(str(fr[7]).rjust(7))
            f.write(str(fr[8]).rjust(7))
            f.write('\n')

    webbrowser.open(outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
