import gzip
import sys

def process(f):
    for line in f:
        if line.startswith("#"):
            print(line[:-1])
        else:
            line = line[:-1].split("\t")
            print("\t".join(line[0:2]+["."]+line[3:]))



infile = sys.argv[1]

#infile = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/merged/merged.testvariants.tested.sorted.uniq.any_variant.sorted.vcf.gz"

if infile[-3:]==".gz":
    with gzip.open(infile) as f:
        process(f)
else:
    with open(infile) as f:
        process(f)

        
