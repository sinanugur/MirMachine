# Output
------
The `MirMachine` main executable will generate GFF annotations (filtered and unfiltered) and some other files.
You will see `results/predictions/` directory which contains:

`filtered_gff/` __High confidence miRNA family predictions after bitscore filtering. (This file is what you need in most cases)__  

`gff/` __All predicted miRNA families.__  

`fasta/` __Both high and low confidence predictions in FASTA format.__  


### Explanation of GFF headers

`
##gff-version 3
# MirMachine version: 0.2.11.2
# CM Models: Built using MirGeneDB 2.1
# Total families searched: 77
# Node: Caenorhabditis
# Model: combined
# Genome file: sample/genomes/ce11.fa
# Species: Astyanax_mexicanus
# Params: /WORKING/apps/condas/sium_conda/bin/MirMachine.py --node Caenorhabditis --species Astyanax_mexicanus --genome sample/genomes/ce11.fa --cpu 20
# miRNAs families searched:
`

