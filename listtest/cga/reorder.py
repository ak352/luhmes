
import fileinput

f = fileinput.input()
print(next(f)[:-1])
count  = 0
for line in f:
    count += 1
    line = line[:-1].split("\t")
    print("\t".join([str(count)] + line[1:]))
    
