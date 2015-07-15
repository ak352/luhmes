infile = "/work/projects/isbsequencing/resources/refGenomes/hg19.fa"
outfile = "/work/projects/isbsequencing/resources/refGenomes/hg19.upper.fa"
print("Input: %s" % infile)
print("Output: %s" % outfile)

out = open(outfile, "w")
for line in open(infile):
    if line.startswith(">"):
        out.write(line)
    else:
        out.write(line.upper())

out.close()        
