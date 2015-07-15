import csv
import gzip
import sys

#ASSEMBLY_ID    GS000022396-ASM
#COSMIC COSMIC v61
#DBSNP_BUILD    dbSNP build 137
#GENOME_REFERENCE       NCBI build 37
#SAMPLE GS02375-DNA_A01
#GENERATED_BY   cgatools
#GENERATED_AT   2013-Sep-06 20:16:46.763584
#SOFTWARE_VERSION       2.4.0.43
#FORMAT_VERSION 2.4
#GENERATED_BY   dbsnptool
#TYPE   VAR-ANNOTATION

# >locus  ploidy  allele  chromosome      begin   end     varType reference       alleleSeq       varScoreVAF     varScoreEAF     varFilter       hapLink xRef    alleleFreq      alternativeCalls
# 1       2       all     chr1    0       10000   no-ref  =       ?
# 2       2       all     chr1    10000   11039   no-call =       ?          
# 720     2       1       chr1    38231   38232   snp     A       G       282     282     PASS            dbsnp.86:rs806727;dbsnp.131:rs77823476  ;
# 720     2       2       chr1    38231   38232   snp     A       G       123     123     PASS            dbsnp.86:rs806727;dbsnp.131:rs77823476  ;      
# 8482    2       1       chr1    568745  568745  ins             CA      336     429     PASS            dbsnp.137:rs200850333   dbsnp:0.090
# 8482    2       2       chr1    568745  568745  ins             CA      146     146     PASS            dbsnp.137:rs200850333   dbsnp:0.090

infile="/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/LP6008092-DNA_G09/Variations/LP6008092-DNA_G09.genome.vcf.gz"
sample = "LP6008092-DNA_G09"

""" Find where header begins """
line = ""
header = None
with gzip.open(infile) as f:
    while line[:6] != "#CHROM":
        pos = f.tell()
        line = next(f)
        header = line[:-1].split("\t")
        
new_header=""
counter = 0
serr = sys.stderr
#TODO: Check header

serr.write("[WARN] Using fake ploidy = 2...\n")
varScoreVAF = "999"
varScoreEAF = "999"
hapLink=""
alleleFreq=""
alternativeCalls=""


with gzip.open(infile) as f:
    f.seek(pos)
    csvreader = csv.DictReader(f, delimiter="\t")
    for record in csvreader:
        counter += 1
        ploidy = 2 #fake
        alleles = [record['REF']]+record['ALT'].split(",")
        xRef = record['ID']
        info = record['INFO'].split(";")
        varFilter = record['FILTER']
        #print info
        if info == ["."] or "END=" not in record['INFO']:
            info_dict = {}
            info_dict['END'] = record['POS']
        else:
            for i,k in enumerate(info):
                info[i] = k.split("=")
                
                if len(info[i])==1:
                    info[i].append(True)
            #print info
            info_dict = dict(info)
        genotype_dict = dict(zip(record['FORMAT'].split(":"), record[sample].split(":")))
        genotype = genotype_dict['GT']
        if record['REF']=='N':
            var_type = "no-ref"
            reference = "="
            alleleSeq= "="
        elif genotype == "0/0":
            var_type = "ref"
            reference = "="
            alleleSeq = "="
        elif genotype == ".":
            var_type = "no-call"
            reference = "="
            alleleSeq = "="
        else:
            #There is a variant
            #For each allele, find differing sequence to get start, stop, ref, alt
            #TODO: special handling of 0-based/1-based for indels
            #print allele=1
            #print allele=2
            pass
        allele = 1 
        #print(record)
        line = [str(counter),
                str(ploidy),
                str(allele),
                record['#CHROM'],
                str(int(record['POS'])-1),
                info_dict['END'],
                var_type,
                reference,
                alleleSeq,
                varScoreVAF,
                varScoreEAF,
                varFilter,
                hapLink,
                xRef,
                alleleFreq,
                alternativeCalls]
        print("\t".join(line)[:-1])
                
