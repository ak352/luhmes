### Pipeline to combine Illumina GVCF and Complete Genomics testvariants format

1. Use ```commands.sh``` to convert to filter the Illumina GVCF file and convert to Complete Genomics testvariants format (depends on module load pipeline)
2. The ```cga/``` directory contains scripts for testing Illumina variants in Complete Genomics using cgatools testvariants
3. The ```gvcftools/``` directory contains scripts for testing Complete Genomics variants against the Illumina gvcf file (depends on GVCF tools merge_variants and a Python script "concordance.py" to check for reference/no-call for non-variant regions)
4. The ```merged/``` directory contains scripts to combine tested variants from step 2 and 3 and remove duplicate records and produce a combine testvariants output file 
5. The ```plink/``` directory contains scripts to convert the merged testvariants file to VCF and perform PLINK Identity by Descent analysis

