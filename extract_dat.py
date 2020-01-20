with open('data_samples/extract_from_test.txt') as file:
    for line in file:
        if not line.strip():
            continue
        else:
            print(line[2:15])
            print(line[2:15] == "Nome Stazione")
            nospace = line.replace(' ', '')
