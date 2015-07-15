#!/bin/bash --login
module load tabix

lpdir=/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/LP6008092-DNA_G09/Variations
lp_snv=$lpdir/LP6008092-DNA_G09.vcf.gz

filter()
{
    # Create a filtered VCF file using PASS
    OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv
    #mkdir -v $OUTDIR
    filt=${lp_snv##*/}
    filt=$OUTDIR/${filt%%.gz}.filt.vcf.gz
    
    echo Filtering...
    ( zgrep "^#" $lp_snv; \
      zgrep -v "^#"  $lp_snv | awk -F"\t" '$7=="PASS"';) | bgzip > $filt
    echo Done.
}

to_tv()
{
    module load lang/Python/2.7.3-ictce-5.3.0
    module load pipeline
    OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv
    input=$1
    temp=/tmp/temp
    output=${input##*/}
    output=$OUTDIR/${output%%.vcf.gz}.testvariants

    echo Writing to $temp...
    zcat $lp_snv | sed 's/:DPI:/:DP:/g' > $temp
    echo Writing to $output...
    python to_testvariants.py $temp $output
    echo Output written to $output

}

# filter
# to_tv $lp_snv
# filt=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv/LP6008092-DNA_G09.filt.vcf.gz
# to_tv $filt
#


# module load lang/Python/2.7.3-ictce-5.3.0
# module load pipeline
# module list












# Convert both filtered and genome file to testvariants
# Perform list using the PASS and VQHIGH and test variants using all the variants

# Annotate using ANNOVAR





# For chromosome-scale changes, compare SVs










