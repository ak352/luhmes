

def get():
    mapper = {}
    for line in open("table.tsv"):
        line = line[:-1].split("\t")
        mapper[tuple(line[:2])] = line[2]

    return mapper
