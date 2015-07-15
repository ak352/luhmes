
#cg = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/gvcf/GS000022396.list.tested.LP6008092-DNA_G09.genome.testvariants.genotype"
cg = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/gvcf/GS000022396.list.tested.vqhigh.LP6008092-DNA_G09.genome.testvariants.genotype"
il = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/LP6008092-DNA_G09.genome.vcf.filt.testvariants.tested"
output="/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/merged/merged.testvariants.tested"



varid = set()
out = open(output, 'w')


with open(cg) as a:
    out.write(next(a)[:-1]+"\tplatform\n")
    for line in a:
        out.write(line[:-1] + "\tcg\n")

with open(il) as b:
    next(b)
    for line in b:
        line = line[:-1].split("\t")
        #print line
        out.write("\t".join(line[:-2] + line[-1:-3:-1] + ["il"])+"\n")
        

    

