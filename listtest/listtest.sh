#!/bin/bash --login
module load cgatools

# OPTIONS
# -h [ --help ]
# Print this help message.

# --beta
# This is a beta command. To run this command, you must pass the --beta
# flag.

# --reference arg
# The reference crr file.

# --output arg (=STDOUT)
# The output file (may be omitted for stdout).

# --variants arg
# The input variant files (may be passed in as argument at the end of the
# 			 command).

# --variant-listing arg
# The output of another listvariants run, to be merged in to produce the
# output of this run.

# --list-long-variants
# In addition to listing short variants, list longer variants as well
#         (10's of bases) by concatenating nearby calls.


var=/work/projects/isbsequencing/luhmes_cell_line/sequence/luhmes_cell_line/GS02375-DNA_A01/GS000022396-ASM/ASM/var-GS000022396-ASM.tsv.bz2
ref=/work/projects/isbsequencing/resources/refGenomes/hg19.crr
OUTDIR=/work/projects/isbsequencing/luhmes_cell_line/users/akrishna/analysis/snv
mkdir -v $OUTDIR
output=$OUTDIR/ukn.list

lister()
{
    echo Listing variants...
    cgatools listvariants --beta --variants $var --reference $ref --output $output
    echo Done.
}

tester()
{
    input=$OUTDIR/ukn.list
    output=$OUTDIR/ukn.list.tested
    echo Testing variants...
    cgatools testvariants --beta --input $input --variants $var --reference $ref --output $output
    echo Done.
}

    


# lister
tester

       
