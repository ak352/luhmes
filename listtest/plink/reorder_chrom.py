import fileinput
from collections import defaultdict

with open("order") as f:
    chroms = [x.strip() for x in next(f)[:-1].split(",")]
    
    # chroms = dict([(y,x) for x,y in enumerate(chroms)])
outfiles = []    
for chrom in chroms:
    outfiles.append(open("/tmp/chrom/%s", "w"))

    
f = fileinput.input()
line = next(f)

while f.startswith("#"):
    print(line[:-1])
    line = next(f)

for line in f:
    line = line[:-1].split("\t")
    chrom = line[0]

        
    variants[line[0]].append(line)

    
for chrom in chroms:
    if chrom in variants:
        for line in variants[chrom]:
            print("\t".join(line))
            
    
    
    

