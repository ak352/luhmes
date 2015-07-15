import sys
from collections import Counter, defaultdict
import get_mapper

def process(line, counter, mapper):
    vartype = line[4]
    cg = line[8]
    il = line[9]
    if cg=="NN" or il=="NN":
        counter[vartype]['no-call'] += 1
    elif cg == "N" or il == "N":
        counter[vartype]['no-call'] += 1
    elif "1" not in cg+il:
        sys.stderr.write("[WARN] No variant found in line %s\n" % "\t".join(line))
    else:
        counter[vartype][mapper[tuple(sorted([cg, il], reverse=True))]] += 1
        
        

# infile = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/gvcf/GS000022396.list.tested.LP6008092-DNA_G09.genome.testvariants"
# infile = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/merged/merged.testvariants.tested.sorted.uniq.any_variant"
infile = sys.argv[1]

counter = defaultdict(Counter)
mapper = get_mapper.get()

with open(infile) as f:
    line = next(f)
    for line in f:
        line = line[:-1].split("\t")
        process(line, counter, mapper)
        

sys.stdout.write("vartype\tconcordant\tdiscordant\tpartial_concordance\n")
for key in sorted(counter.keys()):
    cnt = counter[key]
    weighted_concordant = cnt['Concordant'] + cnt['Partially concordant']
    total = cnt['Concordant'] + cnt['Partially concordant'] + cnt['Discordant']
    pct = weighted_concordant*100./total
    sys.stdout.write("\t".join(map(str,[key, cnt['Concordant'], cnt['Discordant'],
                             cnt['Partially concordant'], cnt['no-call'], pct])) + "\n")

