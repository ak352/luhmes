PATH=/work/projects/isbsequencing/tools/tabix/tabix-0.2.6/:$PATH
PATH=/work/projects/isbsequencing/tools/cgatools/bin/:$PATH
export PATH

ref=/work/projects/isbsequencing/tools/cgatools/ref/hg19.crr
ref_fa=/work/projects/isbsequencing/resources/refGenomes/hg19.upper.fa


merge()
{

    merged=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/merged/merged.testvariants.tested
    merged_sorted=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/merged/merged.testvariants.tested.sorted

    head $merged
    echo ...
    tail $merged

    # ( head -n1 $merged; \
    #   sed '1d' $merged \
    # 	  | sed 's/\tchr\([0-9]\t\)/\tchr0\1/g' \
    # 	  | sort -k2,2 -k3,3n -k4,4n -k5,5 -k6,6 -k7,7 \
    # 	  | sed 's/chr0/chr/g' )  \
    # 	> $merged_sorted 

    
    cmd="python unique.py $merged_sorted > $merged_sorted.uniq"
    echo $cmd
    eval $cmd
    # head $merged_sorted.uniq
    # echo Checking for duplicate records of homozygous variants ...
    # grep -P '\t11\t11' $merged_sorted.uniq | head
    # echo Checking for duplicate records ...
    # cut -f2-7 $merged_sorted.uniq| uniq -d| head
    # wc -l $merged_sorted.uniq
    # grep -P 'NN\tNN' $merged_sorted.uniq
    #
    #
    # grep -P "chr1\t(1243932|3142094|3268109)\t" /work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/cg/GS000022396.list.tested
    # bzgrep -P "chr1\t(1243932|3142094|3268109)\t" /work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/GS02375-DNA_A01/GS000022396-ASM/ASM/var-GS000022396-ASM.tsv.bz2
    # bzcat VQHIGH /work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/GS02375-DNA_A01/GS000022396-ASM/ASM/var-GS000022396-ASM.tsv.bz2| head -n30

    #cmd="grep -P '\tNN\t' /work/projects/isbsequencing/luhmes_cell_line/users/pmay/luhmes_cell_line.variantlist.tested.vqhigh| wc -l"

    #echo $cmd
    #eval $cmd

    
    
    # head 
    
    #TODO: These should not be NNNN? Check GS*.list.tested!
    # cut -f9-10 $merged_sorted.uniq| grep -v N | sort | uniq -c | sort -nr
    # echo ...
    # cut -f9-10 $merged_sorted.uniq| grep  N | sort | uniq -c | sort -nr
    
    #grep -w 38231 $merged_sorted.uniq


}


remove_non_variant()
{
    input=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/merged/merged.testvariants.tested.sorted.uniq
    output=$input.any_variant
    log=$output.log
    cmd="python any_variant.py $input > $output 2>$log"
    echo $cmd
    eval $cmd
    
}

stats()
{
    input=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/merged/merged.testvariants.tested.sorted.uniq.any_variant
    python concordance.py $input
}

tv2vcf()
{
    input=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/merged/merged.testvariants.tested.sorted.uniq.any_variant
    output=$input.vcf
    sorted_output=$input.sorted.vcf
    log=$output.log

    testvariants2vcf=/work/projects/isbsequencing/tools/cgscripts/testvariants2VCF-v2/testvariants2VCF-v2.pl

    # $testvariants2vcf -h
    cmd="sed -i 's/^>//1' $input;"
    cmd="$cmd $testvariants2vcf $input $ref > $output 2> $log;"
    cmd="$cmd bgzip -c $output > $output.gz;"
    #echo $cmd
    #eval $cmd

    # zcat $output.gz| head -n30
    # echo ...
    # zcat $output.gz| tail
    
    cmd='(zcat $output.gz | grep "^#"; zcat $output.gz | grep -v ^"#" | sort -k1,1 -k2,2n;) | bgzip -c >  $sorted_output.gz'
    echo $cmd
    #eval $cmd
    cmd="tabix -fp vcf $sorted_output.gz"
    echo $cmd
    #eval $cmd

    zcat $sorted_output.gz | head -n30
    echo ...
    zcat $sorted_output.gz | tail

    
}
    



# merge
# remove_non_variant
# stats
tv2vcf
