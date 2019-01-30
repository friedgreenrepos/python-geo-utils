import csv
import untangle
import xmltodict
import webbrowser
import sys
import getopt
from geoutils import fill_xml_points, rows2list

def main(argv):
    """
    Update an xml file with the points given as input.
    """
    input_xml = ''
    input_points = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hx:p:o:", ["xml=", "points=" "ofile="])
    except getopt.GetoptError:
        print('xml_filler.py -x <input_xml> -p <input_points> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('xml_filler.py -x <input_xml> -p <input_points> -o <outputfile>')
            sys.exit()
        elif opt in ("-x", "--xml"):
            input_xml = arg
        elif opt in ("-p", "--points"):
            input_points = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    points = rows2list(open(input_points))

    fill_xml_dict = fill_xml_points(points=points, open_xml=open(input_xml))

    fill_xml_xml = xmltodict.unparse(fill_xml_dict, pretty=True)

    with open(outputfile, "w+") as f:
        f.write(fill_xml_xml)

    webbrowser.open(outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
