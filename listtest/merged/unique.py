import fileinput
from collections import Counter

def report(buf, count, cnt):
    chosen = buf[0]
    """ If duplicates, choose the version from CG as the VCF to testvariants converts 1N to 10? """
    for var in buf:
        if var[10] == "cg":
            chosen = var
    count += 1

    is_print = False
    ref = buf[0][8:10]
    for var in buf[1:]:
        if ref != var[8:10]:
            is_print= True
    if is_print:
        cnt[var[4]] += 1
        # for var in buf:
        #     print("\t".join(var))
        # print ""
        
            
    print("\t".join([str(count)] + chosen[1:]))
    return count


test = False
if not test:
    f = fileinput.input()
else:
    f = open("/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/merged/merged.testvariants.tested.sorted")

print(next(f)[:-1])
count  = 0
prev = None
buf = []


cnt = Counter()

for line in f:
    line = line[:-1].split("\t")
    variant = line[1:7]+line[8:10]

    if prev and prev[:6]!=variant[:6]:
        if test:
            pass
            # print "prev = ", prev
            # print "variant = ", variant
        count = report(buf, count, cnt)
        buf = []
        
    buf.append(line)    
    prev = variant

""" TODO: last variant group """
""" TODO: check why chr1, 923978 insertion is 11 in cgatools list test, and 01 in cgatools test """
# print cnt.most_common
