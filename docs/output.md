# Output

The `MirMachine` main executable will generate GFF annotations (filtered and unfiltered) and some other files.
You will see `results/predictions/` directory which contains:

`filtered_gff/` __High confidence miRNA family predictions after bitscore filtering. (This file is what you need in most cases)__  

`gff/` __All predicted miRNA families.__  You can access all the predictions without filtering.

`fasta/` __Both high and low confidence predictions in FASTA format.__  Both predictions from filtered and unfiltered are included and you access FASTA sequences. See explanation of FASTA identifiers.


## Explanation of GFF files

**Header**
```
##gff-version 3
# MirMachine version: 0.2.11.2 (MirMachine version)
# CM Models: Built using MirGeneDB 2.1 (DB version, usually suggests new families were included)
# Total families searched: (Total families searched for this run)
# Node: (Node name given)
# Model: (selected model)
# Genome file: (genome file location)
# Species: (species name given)
# Params: (Command line paramaters)
# miRNAs families searched: (searched families)
```

```
chrI    cmsearch        ncRNA   6162306 6162369 45.3    -       .       gene_id=Mir-92.PRE;E-value=5.5e-07;sequence_with_30nt=TGCTGAAAATCGTCCGAAGATATCAGGATCAGGCCTTGGCTGATTGCAAAATTGTTCACCGTGAAAATTAAATATTGCACTCTCCCCGGCCTGATCTGAGAGTAAGGCGAAGCTGAATTGACTT
```

## FASTA files



