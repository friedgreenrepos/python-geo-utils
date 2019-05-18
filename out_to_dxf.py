#!/usr/bin/env python
import csv
import sys
import webbrowser
import getopt


def main(argv):
    """
    Create a .DXF file from a .OUT one.
    """
    outfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('swap_coordinates.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('swap_coordinates.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            outfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    height = 0.07
    layer_1 = 1  # layer points
    layer_2 = 2  # layer text

    # setting up header
    header = "  0\nSECTION\n2\nHEADER\n  9\n$PDSIZE\n 40\n2.0\n  9\n$PDMODE\n 70\n30\n  9\n$TEXTSIZE\n 40\n.02\n  9\n$TEXTSTYLE\n  7\nSTANDARD\n  0\nENDSEC\n  0\nSECTION\n2\nENTITIES"
    # setting up entity base format
    base_format = "\n0\nPOINT\n8\n{layer_1}\n10\n{est}\n20\n{nord}\n0\nTEXT\n8\n{layer_2}\n10\n{est}\n20\n{nord}\n40\n{altezza}\n1\n{name}"

    with open(outfile) as out_file:
        # read .out file
        out_reader = csv.reader(out_file, delimiter=',')
        # jump first 4 lines
        for i in range(4):
            next(out_reader)

        # formatted string will stored here and then written to file.
        out_array = []

        for row in out_reader:
            entity = base_format.format(layer_1=layer_1, layer_2=layer_2,
                                        est=row[1], nord=row[3],
                                        altezza=height, name=row[0])
            out_array.append(entity)

    with open(outputfile, 'w+') as f:
        f.write(header)
        for ent in out_array:
            f.write(ent)

    webbrowser.open(outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
