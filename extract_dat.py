def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


with open('data_samples/extract_from.txt', 'r') as input:
    # extract_lst = []
    for line in input:
        if not line.strip():
            continue
        if line[2:15] == "Nome Stazione":
            # mentre nome stazione è sempre uguale (speriamo)
            # n_staz potrebbe non avere sempre 3 cifre
            n_staz = line[17:].strip()
            staz = [line[2:15], n_staz]
            # output.write("1")
            # output.write("|")
            # output.write(n_staz)
            # output.write("|")
            # output.write('\n')
            extract_lst.append(staz)
        elif represents_int(line[24:25]):
            info = line[24:117].split()
            # output.write(info[0])
            # output.write("|")
            # output.write(info[4])
            # output.write("|")
            # output.write(info[5])
            # output.write("|")
            # output.write('\n')
            extract_lst.append(coords)
