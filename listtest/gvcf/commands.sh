PATH=/work/projects/isbsequencing/tools/gvcftools/gvcftools-0.16/bin/:$PATH
PATH=/work/projects/isbsequencing/tools/vcftools/bin/:$PATH
PATH=/work/projects/isbsequencing/tools/cgatools/bin/:$PATH
PATH=/work/projects/isbsequencing/tools/tabix/tabix-0.2.6/:$PATH
PERL5LIB=/work/projects/isbsequencing/tools/vcftools/lib/perl5/site_perl/:$PERL5LIB
export PATH
export PERL5LIB

ref=/work/projects/isbsequencing/tools/cgatools/ref/hg19.crr
ref_fa=/work/projects/isbsequencing/resources/refGenomes/hg19.upper.fa

# Query positions 
#gvcftools

listtest()
{
    variants=/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/GS02375-DNA_A01/GS000022396-ASM/ASM/var-GS000022396-ASM.tsv.bz2
    OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg/
    mkdir -v $OUTDIR
    output=$OUTDIR/GS000022396.list
    cgatools listvariants --beta --reference $ref --output $output --variants $variants

    input=$OUTDIR/GS000022396.list
    output=$input.tested
    cgatools testvariants --beta --reference $ref --input $input --output $output --variants $variants
}

annotate_filter()
{
    input=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg//GS000022396.list.tested
    variants=/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/GS02375-DNA_A01/GS000022396-ASM/ASM/var-GS000022396-ASM.tsv.bz2
    output=$input.vqhigh.temp
    # cgatools join -h
    # bzcat $variants | head -n30
    cmd="cgatools join --beta --match chromosome:chromosome --match varType:varType --match reference:reference               --match alleleSeq:alleleSeq --overlap begin,end:begin,end \
             --input $input $variants \
    	     --output $output --overlap-mode allow-abutting-points --select A.*,B.varFilter -a"
    #echo $cmd
    #eval $cmd

    input=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg//GS000022396.list.tested.vqhigh.temp
    output=${input%%.temp}
    grep -P '^(>variantId|[0-9]+)\t' $input \
    	| awk -F"\t" '$1==">variantId" || $10=="PASS"' \
    	| uniq | python reorder.py | cut -f 1-9 \
	| sed 's/^>//1' > $output
    
    
    wc -l $output
    # bzcat $variants| head -n20
}



tv2vcf()
{
    OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg/
    # input=$OUTDIR/GS000022396.list.tested
    # output=$OUTDIR/GS000022396.vcf
    # log=$OUTDIR/GS000022396.log.txt

    input=$OUTDIR/GS000022396.list.tested.vqhigh
    output=$OUTDIR/GS000022396.vqhigh.vcf
    log=$OUTDIR/GS000022396.vqhigh.log.txt


    testvariants2vcf=/work/projects/isbsequencing/tools/cgscripts/testvariants2VCF-v2/testvariants2VCF-v2.pl

    $testvariants2vcf -h
    cmd="$testvariants2vcf $input $ref > $output 2> $log;"
    cmd="$cmd bgzip -f $output;"
    echo $cmd
    eval $cmd
    cmd='(zcat $output.gz | grep "^#"; zcat $output.gz | grep -v ^"#" | sort -k1,1 -k2,2n;) | bgzip -fc >  $output.sorted.gz'
    echo $cmd
    eval $cmd
    cmd="tabix -fp vcf $output.sorted.gz"
    echo $cmd
    eval $cmd
}


tv2bed()
{
    OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg/
    input=$OUTDIR/GS000022396.list.tested
    output=$OUTDIR/GS000022396.list.tested.bed
    output_head=$OUTDIR/GS000022396.list.tested.head.bed
    # Use start-1 for the interval to include the reference base for indels and end-1 to include the position for insertions
    sed '1d' $input | cut -f2-4 | awk -F"\t" 'BEGIN{OFS="\t"}{print $1, $2-1, $3+1}' > $output
    sed '1d' $input | cut -f2-4 | awk -F"\t" 'BEGIN{OFS="\t"}{print $1, $2-1, $3+1}'| head > $output_head
}


merge()
{
    OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg/
    # vcf=$OUTDIR/GS000022396.vcf.sorted.gz
    vcf=$OUTDIR/GS000022396.vqhigh.vcf.sorted.gz
    gvcf=/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/LP6008092-DNA_G09/Variations/LP6008092-DNA_G09.genome.vcf.gz
    bed=$OUTDIR/GS000022396.list.tested.bed
    
    output=$bed.LP6008092-DNA_G09.break_blocks.vcf.gz
    #zcat $gvcf | head


    #zcat $gvcf | head -n2000| bgzip  > test.gvcf
    # cmd="time break_blocks --region-file $bed --ref $ref_fa --exclude-off-target < <( zcat $gvcf) | bgzip -c > $output;"
    # cmd="$cmd tabix -fp vcf $output"
    # echo $cmd
    # #eval $cmd

    # vcf2=$output
    # output=${vcf%%vcf.gz}.${vcf2##*/}
    # cmd="vcf-merge $vcf $vcf2 | bgzip -c > $output"
    # echo $cmd
    #eval $cmd


    OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/gvcf/
    # output=$OUTDIR/GS000022396.vcf.sorted.LP6008092-DNA_G09.genome.vcf.gz
    output=$OUTDIR/GS000022396.vqhigh.vcf.sorted.LP6008092-DNA_G09.genome.vcf.gz

    merge_variants -h
    echo Writing to $output ...
    cmd="merge_variants --ref $ref_fa --murdock --input $vcf $gvcf | cut -f-9,11 | bgzip -c > $output"
    echo $cmd
    eval $cmd

    
}

vcf2tv()
{
    module load lang/Python/2.7.3-ictce-5.3.0
    module load pipeline
    OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg
    #input=$OUTDIR/GS000022396.list.tested.bed.LP6008092-DNA_G09.break_blocks.vcf.gz
    # input=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/gvcf//GS000022396.vcf.sorted.LP6008092-DNA_G09.genome.vcf.gz
    input=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/gvcf//GS000022396.vqhigh.vcf.sorted.LP6008092-DNA_G09.genome.vcf.gz
    temp=/tmp/temp.gz
    #output=${input##*/}
    #output=$OUTDIR/${output%%.vcf.gz}.testvariants
    
    output=${input%%.vcf.gz}.testvariants

    echo Input:
    zcat $input | head -n30
    echo ...
    zcat $input | tail -n30

    
    echo Writing to $temp...
    zcat $input | sed 's/:DPI:/:DP:/g'  | bgzip -fc > $temp
    echo Writing to $output...
    python to_testvariants.py $temp $output
    sed -i 's/^>//1' $output
    echo Output written to $output
    head -n30 $output
    echo ...
    tail -n30 $output
    

}

join()
{

    # OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg
    # testvariants=$OUTDIR/GS000022396.list.tested
    # break_blocks_testvariants=$OUTDIR/GS000022396.list.tested.bed.LP6008092-DNA_G09.break_blocks.testvariants
    # output=$OUTDIR/GS000022396.list.tested.LP6008092-DNA_G09.break_blocks

    # cmd="cgatools join --beta -a --match chromosome:chromosome --overlap begin,end:begin,end \
    # 	     --input  $testvariants $break_blocks_testvariants \
    # 	     --output $output"
    # echo $cmd
    # eval $cmd

    INDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg
    OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/gvcf
    # testvariants=$INDIR/GS000022396.list.tested
    testvariants=$INDIR/GS000022396.list.tested.vqhigh
    # merge_variants_output=$OUTDIR/GS000022396.vcf.sorted.LP6008092-DNA_G09.genome.testvariants
    merge_variants_output=$OUTDIR/GS000022396.vqhigh.vcf.sorted.LP6008092-DNA_G09.genome.testvariants
    # output=$OUTDIR/GS000022396.list.tested.LP6008092-DNA_G09.genome.testvariants
    output=$OUTDIR/GS000022396.list.tested.vqhigh.LP6008092-DNA_G09.genome.testvariants
    sample=LP6008092-DNA_G09
    # Overlap mode allows abutting points in order to match insertions where begin==end
    cmd="cgatools join --beta -a --match chromosome:chromosome --overlap begin,end:begin,end \
    	     --input  $testvariants $merge_variants_output \
             --select A.*,B.* \
             --overlap-mode allow-abutting-points \
    	     --output $output"
    echo $cmd
    eval $cmd
    head $output
    echo ...
    tail $output
    
    
    

    
}

test_allele()
{
    python 

}    



# listtest
# annotate_filter
# tv2vcf
# tv2bed
# merge
# vcf2tv
join


