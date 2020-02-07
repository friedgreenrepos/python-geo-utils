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
                extract_lst.append("stazione")
                extract_lst.append(split_line[2])
            if len(split_line) >= 6 and represents_int(split_line[0]):
                extract_lst.append(line.split()[0])
                extract_lst.append(line.split()[4])
                extract_lst.append(line.split()[5])

