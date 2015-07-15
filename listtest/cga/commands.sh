# Uses cgatools testvariants to check for the positions of SNVs found by Illumina in CG dataset

cgatools=/work/projects/isbsequencing/tools/cgatools/bin/cgatools
cg=/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/GS02375-DNA_A01/GS000022396-ASM/ASM/var-GS000022396-ASM.original.tsv.bz2
#/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/GS02375-DNA_A01/GS000022396-ASM/ASM/var-GS000022396-ASM-sorted.tsv.gz
#/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/GS02375-DNA_A01/GS000022396-ASM/ASM/var-GS000022396-ASM.tsv.bz2
filt=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/LP6008092-DNA_G09.genome.vcf.filt.testvariants
output=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/LP6008092-DNA_G09.genome.vcf.filt.testvariants.tested
ref=/work/projects/isbsequencing/tools/cgatools/ref/hg19.crr
#ref=/work/projects/isbsequencing/tools/cgatools/ref/build37.crr
#/work/projects/isbsequencing/resources/refGenomes/hg19.crr
#head $filt



#$cgatools decodecrr --reference $ref --range chrM:72-73
#cgatools listcrr $ref > order


bzcat $cg | head -n20
(head -n1 $filt; sed '1d' $filt \ #| grep -vw chrM  \
     | sed 's/\tchr\([0-9]\)\t/\tchr0\1\t/g' | sort -k2,2 -k3,4n \
     | sed 's/chr0/chr/g') > $filt.wmt
head $filt.wmt
wc -l  $filt.wmt

# allow abutting points
cmd="time $cgatools testvariants --beta --reference $ref --input $filt.wmt --output $output --variants $cg"
echo $cmd
eval $cmd





