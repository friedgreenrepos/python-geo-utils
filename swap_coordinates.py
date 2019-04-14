#!/usr/bin/env python
import csv
# import webbrowser
# import sys
# import getopt
# from itertools import combinations
# from geoutils import (
#     rows2list,
#     comb2dist_tuple_list,
#     get_dup_list
# )

lines = [line.rstrip('\n') for line in open('data_samples/Layoutnew2.lmk')]
header = []
for i in range(0, 14):
    ln = lines.pop(0)
    header.append(ln)

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

with open('tmp_csv.csv', 'w+') as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerows(final_array)


with open('data_samples/PF1819_d.txt') as f:
    reader_f = csv.reader(f, delimiter=',')
    with open('tmp_csv.csv') as tmp_csv:
        reader_tmp = csv.DictReader(tmp_csv, delimiter=';')

    # per ogni riga del file PF1819.txt
    # - paddo di 0 il primo elemento
    # - lo cerco nel file tmp_csv
    # - se lo trovo sostituisco x[mm], y[mm] con 2° e 3° elemento
    #   del file .txt
    # - altrimenti scrivo una nuova riga in tmp_csv con
    #   numero paddato, x, y

    # for r_f in reader_f:
    #     r_0 = str(r_f[0]).zfill(6)
    #     for r_t in reader_tmp:
    #         if r_0 == r_t['globID']:
    #             r_f




# def main(argv):
#     """
#     Swap x, y coordinates of space-delimited csv file with new ones passed
#     in csv file as input .
#     """
#     inputfile_1 = ''
#     inputfile_2 = ''
#     outputfile = ''
#     try:
#         opts, args = getopt.getopt(argv, "hi:s:o:", ["ifile=", "sfile=", "ofile="])
#     except getopt.GetoptError:
#         print('swap_coordinates.py -i <inputfile> -s <swapfile> -o <outputfile>')
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-h':
#             print('swap_coordinates.py -i <inputfile> -s <swapfile> -o <outputfile>')
#             sys.exit()
#         elif opt in ("-i", "--ifile"):
#             inputfile = arg
#         elif opt in ("-s", "--sfile"):
#             swapfile = arg
#         elif opt in ("-o", "--ofile"):
#             outputfile = arg
#
#
#     webbrowser.open(outputfile)
#
#
# if __name__ == "__main__":
#     main(sys.argv[1:])
