# miRmachine
Command line to tool detect miRNA homolog sequences.

Installation
------------

`conda env create -f environment.yaml`

Quick start example
-------------------
```
git clone https://github.com/sinanugur/miRmachine.git
cd miRmachine
miRmachine-main.py -n Caenorhabditis -s Caenorhabditis_elegans --genome data/genomes/ce11.fasta -m proto --cpu 20
```

Output
------
The `miRmachine` main executable will generate GFF annotations (filtered and unfiltered) and some other files.
