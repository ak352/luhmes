import sys

# infile = "/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/merged/merged.testvariants.tested.sorted.uniq"
infile = sys.argv[1]

count = 0
num_pass = 0
num_fail = 0

with open(infile) as f:
    print("\t".join(next(f)[:-1].split("\t")[:10]))
    for line in f:
        count += 1
        
        line = line[:-1].split("\t")
        passed = False
        for x in line[8:10]:
            if "1" in x:
                passed = True
        if passed:
            num_pass += 1
            print("\t".join([str(num_pass)] + line[1:10]))
        else:
            num_fail += 1

sys.stderr.write("Filtering variants that were not found in either platform:\n")
sys.stderr.write("Total variants = %d\n" % count)            
sys.stderr.write("Variants passing the filter = %d\n" % num_pass)            
sys.stderr.write("Variants failing the filter = %d\n" % num_fail)            

        
