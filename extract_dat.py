def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


with open('data_samples/extract_from_test.txt', 'r') as input_file:
    extract_lst = []
    for line in input_file:
        if not line.strip():
            continue
        else:
            split_line = line.split()
            if (len(split_line) == 3
                    and split_line[0] == "Nome"
                    and split_line[1] == "Stazione:"):
                extract_lst.append("s")
                extract_lst.append(split_line[2])
            if len(split_line) >= 6 and represents_int(split_line[0]):
                extract_lst.append("p")
                extract_lst.append(line.split()[0])
                extract_lst.append(line.split()[4])
                extract_lst.append(line.split()[5])

with open('data_samples/extract_to_test.dat', 'w+') as output_file:
    extract_len = len(extract_lst)
    for index, el in enumerate(extract_lst):
        if el == "s":
            output_file.write("1")
            output_file.write("|")
            output_file.write(extract_lst[index + 1])
            output_file.write("|")
            output_file.write("\n")
        elif el == "p":
            output_file.write("2")
            output_file.write("|")
            for i in range(1, 4):
                output_file.write(extract_lst[index + i])
                output_file.write("|")
            output_file.write("\n")
