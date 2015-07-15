import sys
from collections import Counter, defaultdict
import get_mapper

def process(buf, counter, mapper, out):
    vartype = buf[0].split("\t")[4]

    genotype = None
    has_nn = False
    has_ref = False

    if vartype in ["snp", "ins", "del"] or True:
        """ Check if any of the overlapping variants is a SNV """
        for var in buf:
          var = var.split("\t")
          #print list(enumerate(var))
          if var[1:7] == var[10:16]:
            genotype = var[17]
          if var[13]=="none":
            if var[17] == "NN":
                has_nn = True
            if var[17] == "00":
                has_ref = True
            
        if not genotype:
          #assert has_nn != has_ref, buf
          """ NN has priority over 00 """
          if has_nn:
            genotype = "NN"
          elif has_ref:
            genotype = "00"
          else:
              genotype = "00"

        out.write("\t".join(var[:9]+[genotype]) + "\n")
        
        if var[8]=="NN" or genotype=="NN":
            counter[vartype]['no-call'] += 1
        elif var[8] == "N" or genotype == "N":
            counter[vartype]['no-call'] += 1
        elif "1" not in var[8]+genotype:
            pass
        else:
            counter[vartype][mapper[tuple(sorted([var[8], genotype], reverse=True))]] += 1
              
            
    
def report(line, out):
    for k in [sys.stderr, out]:
        k.write(line + "\n")
        

# infile = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/gvcf/GS000022396.list.tested.LP6008092-DNA_G09.genome.testvariants"
infile = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/gvcf/GS000022396.list.tested.vqhigh.LP6008092-DNA_G09.genome.testvariants"
outfile = infile + ".genotype"
logfile = outfile + ".log"

log = open(logfile, 'w')
out = open(outfile, 'w')


report("Input: " + infile, log)
report("Output: " + outfile, log)
report("Log: " + logfile, log)

prev = None     
buf = []


lines = 0
loglines = 10000000
counter = defaultdict(Counter)
mapper = get_mapper.get()

with open(infile) as f:
    line = next(f)
    line = line[:-1].split("\t")
    out.write("\t".join(line[:9]+[line[17]])+"\n")
    for line in f:
        line = line[:-1].split("\t")
        lines += 1
        if prev and line[0]!=prev:
            process(buf, counter, mapper, out)
            #print ""
            buf = []
        buf.append("\t".join(line))
        prev = line[0]


        if lines % loglines == 0:
            sys.stderr.write("%d lines processed...\n" % lines)

    process(buf, counter, mapper, out)

    log.write("vartype\tconcordant\tdiscordant\tpartial_concordance\n")
    for key in sorted(counter.keys()):
        #print key

        #print counter[key].most_common()
        cnt = counter[key]
        weighted_concordant = cnt['Concordant'] + cnt['Partially concordant']
        total = cnt['Concordant'] + cnt['Partially concordant'] + cnt['Discordant']
        pct = weighted_concordant*100./total

        # print "\t".join(map(str,[key, cnt['concordant'], cnt['discordant'], cnt['partial_concordant'], \
        #                          cnt['other'],pct]))
        # log.write("\t".join(map(str,[key, cnt['concordant'], cnt['discordant'], cnt['partial_concordant'], \
        # cnt['other'],pct])) + "\n")
        log.write("\t".join(map(str,[key, cnt['Concordant'], cnt['Discordant'],
                                 cnt['Partially concordant'], cnt['no-call'], pct])) + "\n")

