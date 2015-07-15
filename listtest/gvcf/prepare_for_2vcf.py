import gzip
import sys

infile = sys.argv[1]
# infile =  "/tmp/temp.gz"
with gzip.open(infile) as f:
    line = next(f)
    while line.startswith("##"):
        print(line[:-1])
        line = next(f)
    # print(line[:-1])
    print(line[:-1] + "\tfake")

    prev = None
    buf = []
    for line in f:
        line = line[:-1].split("\t")
        chrom, pos, iden, ref, alt = line[:5]
        if alt == ".":
            line[4] = "X"
            fields = line[9].split(":")[:]
            fields[0] = "1/1"
            fields = ":".join(fields)
            line.append(fields)
        else:
            line.append(".")
        print("\t".join(line))
        
