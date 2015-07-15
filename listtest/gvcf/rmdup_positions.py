import gzip


def choose(buf):
    dups = 0
    for k in buf:
        if k[4]!=".":
            dups += 1
            #print("\t".join(k))
    if dups > 1:
        print buf


            
# get the gvcf
# Removing the redundant reference record still leaves the case of indel conflicts

infile = "/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/LP6008092-DNA_G09/Variations/LP6008092-DNA_G09.genome.vcf.gz"


with gzip.open(infile) as f:
    line = next(f)
    while line.startswith("##"):
        #print(line[:-1])
        line = next(f)
    print(line[:-1])

    prev = None
    buf = []
    for line in f:
        line = line[:-1].split("\t")
        #print line
        if line[:2] != prev:
            if len(buf)>1:
                choose(buf)
            else:
                pass #print(buf)
            buf = []
        buf.append(line)
            
        prev = line[:2]
