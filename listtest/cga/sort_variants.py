import bz2
import csv
from collections import defaultdict
import os

out_dir="/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg"


def get_order():
    order_file="order"
    order  = []
    with open(order_file) as f:
        next(f)
        for line in f:
            line = line[:-1].split()
            order.append(line[1])
            #order[line[1]] = int(line[0])
    return order

def divide():

    infile="/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/GS02375-DNA_A01/GS000022396-ASM/ASM/var-GS000022396-ASM.tsv.bz2"


    out = defaultdict(list)
    with bz2.BZ2File(infile) as f:
        line = next(f)
        while not line.startswith(">"):
            print(line[:-1])
            line = next(f)

        d = defaultdict(list)
        for line in f:
            line = line[:-1].split("\t")
            chrom = line[3]
            if chrom not in out:
                out[chrom].append(out_dir + "/" + chrom)
                out[chrom].append(open(out[chrom][0], "a"))
                print("Writing to " + chrom)
            out[chrom][1].write("\t".join(line))
        #d[line[3]].append("\t".join(line[1:]))
    return out

def output(order):
    count = 0
    for chrom in order:
        out_file = out_dir+"/"+chrom
        if os.path.exists(out_file):
            for line in open(out_file):
                count += 1
                print("\t".join([str(count)] + line.split("\t")[1:]))
                
if __name__ ==  "__main__":
    order = get_order()
    #out = divide()
    output(order)
            


            
    
