lpdir=/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/LP6008092-DNA_G09/Variations
lp_sv=$lpdir/LP6008092-DNA_G09.SV.vcf.gz
lp_snv=$lpdir/LP6008092-DNA_G09.genome.vcf.gz

#ls $lpdir
#zcat $lp_sv| grep -v '^##' | head| sed 's/refseq_gene_id=[0-9,]\+//g' #| cut -f1-4| cat -n 
#zgrep -P '^#CHROM' $lp_sv| sed 's/\t/\n/g'| cat -n 
#zcat $lp_sv| grep -v '^#'| head | cut -f5 | sort | uniq -c 

zgrep -oP 'SVTYPE=[^;]+' $lp_sv| sort | uniq -c
zgrep -oP 'SVTYPE=[^;]+' $lp_sv| wc -l 

zgrep -v '^#'  $lp_sv | wc -l 

