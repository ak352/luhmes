import sys
from collections import Counter, defaultdict

def process(buf, counter):
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
            
              
            
        # if len(buf)!=1:
        #   sys.stderr.write("[WARN] SNV has multiple matches in break_blocks file - \n%s\n" % buf[0])
        #   for line in buf[1:]:
        #     sys.stderr.write("%s\n" % line)
        #   sys.stderr.write("\n")
        #print "\t".join(buf[0].split("\t")[:9]+[genotype])
        if "N" not in var[8] and "N" not in genotype:
            if var[8]==genotype:
                counter[vartype]["concordant"] += 1
            else:
                counter[vartype]["discordant"] += 1
        else:
            if "1" in var[8] and "1" in genotype:
                counter[vartype]["partial_concordant"] += 1
            else:
                counter[vartype]["other"] += 1
    # if vartype == "ins":
    #     for k in buf:
    #         print k
    #     print "------------------------"    
            
        #print "\n".join(buf)
    


infile = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg/GS000022396.list.tested.LP6008092-DNA_G09.break_blocks"
outfile = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg/GS000022396.list.tested.LP6008092-DNA_G09.break_blocks.tested"
logfile = outfile + ".log"

log = open(logfile, 'w')
out = open(outfile, 'w')


prev = None     
buf = []


lines = 0
loglines = 10000000
counter = defaultdict(Counter)
with open(infile) as f:
    next(f)
    for line in f:
        line = line[:-1].split("\t")
        lines += 1
        if prev and line[0]!=prev:
            process(buf, counter)
            #print ""
            buf = []
        buf.append("\t".join(line))
        prev = line[0]


        if lines % loglines == 0:
            sys.stderr.write("%d lines processed...\n" % lines)



    print "vartype\tconcordant\tdiscordant\tpdis\tother\tpct_conrdance"    
    for key in sorted(counter.keys()):
        #print key

        #print counter[key].most_common()
        cnt = counter[key]
        pct = cnt['concordant']*100./(cnt['concordant']+cnt['discordant'])

        print "\t".join(map(str,[key, cnt['concordant'], cnt['discordant'], cnt['partial_concordant'], \
                                 cnt['other'],pct]))
    
	    """ TODO: handle insertions - recorded as subs in Illumina """ 
        """ tawk '$5=="ins"'  /work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg/GS000022396.list.tested.LP6008092-DNA_G09.break_blocks| less """
    
