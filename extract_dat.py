with open('data_samples/extract_from_test.txt') as input:
    with open('data_samples/extract_to_test.dat') as output:
        for line in input:
            if not line.strip():
                continue
            elif line[2:15] == "Nome Stazione":
                n_staz = line[17:].strip()
