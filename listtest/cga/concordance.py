import sys
from collections import Counter, defaultdict
import get_mapper



def process(buf, counter, mapper):
    vartype = buf[0].split("\t")[4]

    genotype = None
    has_nn = False
    has_ref = False

    if vartype in ["snp", "ins", "del"] or True:
        """ Check if any of the overlapping variants is a SNV """
        for var in buf:
          var = var.split("\t")
          #print list(enumerate(var))
          genotype = var[9]
            
              
            
        # if len(buf)!=1:
        #   sys.stderr.write("[WARN] SNV has multiple matches in break_blocks file - \n%s\n" % buf[0])
        #   for line in buf[1:]:
        #     sys.stderr.write("%s\n" % line)
        #   sys.stderr.write("\n")
        #print "\t".join(buf[0].split("\t")[:9]+[genotype])
        if var[8]=="NN" or genotype=="NN":
            counter[vartype]['no-call'] += 1
        elif var[8] == "N" or genotype == "N":
            counter[vartype]['no-call'] += 1
            
        else:
            counter[vartype][mapper[(var[8], genotype)]] += 1
        # if "N" not in var[8] and "N" not in genotype:
        #     if var[8]==genotype:
        #         counter[vartype]["concordant"] += 1
        #     elif "1" in var[8] and "1" in genotype:
        #         counter[vartype]["partial_concordant"] += 1
        #     else:
        #         counter[vartype]["discordant"] += 1
        # else:
        #     if "1" in var[8] and "1" in genotype:
        #         counter[vartype]["partial_concordant"] += 1
        #     else:
        #         counter[vartype]["other"] += 1
    # if vartype == "ins":
    #     for k in buf:
    #         print k
    #     print "------------------------"    
            
        #print "\n".join(buf)
    
def report(line, out):
    for k in [sys.stderr, out]:
        k.write(line + "\n")
        

infile = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/LP6008092-DNA_G09.genome.vcf.filt.testvariants.tested"
outfile = infile + ".stats"
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
    next(f)
    for line in f:
        line = line[:-1].split("\t")
        lines += 1
        if prev and line[0]!=prev:
            process(buf, counter, mapper)
            #print ""
            buf = []
        buf.append("\t".join(line))
        prev = line[0]


        if lines % loglines == 0:
            sys.stderr.write("%d lines processed...\n" % lines)



    # out.write("vartype\tconcordant\tdiscordant\tpdis\tother\tpct_concordance\n")
    out.write("vartype\tconcordant\tdiscordant\tpartial_concordance\n")
    for key in sorted(counter.keys()):
        #print key

        #print counter[key].most_common()
        cnt = counter[key]
        weighted_concordant = cnt['Concordant'] + cnt['Partially concordant']
        total = cnt['Concordant'] + cnt['Partially concordant'] + cnt['Discordant']
        pct = weighted_concordant*100./total

        # print "\t".join(map(str,[key, cnt['concordant'], cnt['discordant'], cnt['partial_concordant'], \
        #                          cnt['other'],pct]))
        # out.write("\t".join(map(str,[key, cnt['concordant'], cnt['discordant'], cnt['partial_concordant'], \
        # cnt['other'],pct])) + "\n")
        out.write("\t".join(map(str,[key, cnt['Concordant'], cnt['Discordant'],
                                 cnt['Partially concordant'], cnt['no-call'], pct])) + "\n")












        
