#!/usr/bin/env python
import csv


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

with open('data_samples/tmp_csv.csv', 'w+') as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(final_array)


def matching_row(el, index, open_csv):
    reader = csv.DictReader(open_csv)
    for row in reader:
        if el == row[index]:
            return row
    return None

# per ogni riga del file PF1819.txt
# - paddo di 0 il primo elemento
# - lo cerco nel file tmp_csv
# - se lo trovo sostituisco x[mm], y[mm] con 2° e 3° elemento
#   del file .txt
# - altrimenti scrivo una nuova riga in tmp_csv con
#   numero paddato, x, y


with open('data_samples/PF1819_d.txt') as swap_csv:
    swap_reader = csv.reader(swap_csv, delimiter=',')
    final_rows = []
    for swap_row in swap_reader:
        r_0 = str(swap_row[0]).zfill(6)
        tmp_row = matching_row(r_0, 'globID', open('data_samples/tmp_csv.csv'))
        if tmp_row is not None:
            swapped_row = [
                tmp_row['globID'],
                swap_row[1],
                swap_row[2],
                tmp_row['type'],
                tmp_row['subtype'],
                tmp_row['size[mm]'],
                tmp_row['layer1'],
                tmp_row['layer2'],
                tmp_row['layer3'],
            ]
            final_rows.append(swapped_row)
        else:
            default_row = [
                r_0,
                swap_row[1],
                swap_row[2],
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
            ]
            final_rows.append(default_row)

with open('data_samples/final_swap.csv', 'w+') as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(final_rows)

with open('data_samples/final_swap.lmk', w+) as f:
    


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
