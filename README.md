# MirMachine
A command line to tool detect miRNA homologs in genome sequences.

Installation
------------
To create required environment using Anaconda:

```
conda env create -f environment.yaml
conda activate mirmachine
```

Then clone git repo:
```
git clone https://github.com/sinanugur/miRmachine.git
cd miRmachine
```

Quick start example
-------------------
You can run miRmachine directly inside the cloned directory.
```
bin/miRmachine-main.py -n Caenorhabditis -s Caenorhabditis_elegans --genome data/genomes/ce11.fasta -m proto --cpu 20
```

Options and Arguments
---------------------
```
Usage:
    mirmachine.py --node <text> --species <text> --genome <text> [--model <text>] [--cpu <integer>] [--add-all-nodes] [--dry]
    mirmachine.py --print-all-nodes
    mirmachine.py (-h | --help)
    mirmachine.py --version

Arguments:
    -n <text>, --node <text>              Node name. (e.g. Caenorhabditis)
    -s <text>, --species <text>           Species name. (e.g. Caenorhabditis_elegans)
    -g <text>, --genome <text>            Genome fasta file location (e.g. data/genome/example.fasta)
    -m <text>, --model <text>             Model type: deutero, proto, combined [default: proto]
    -c <integer>, --cpu <integer>         CPUs. [default: 2]

Options:
    -a --add-all-nodes                 Move on the tree both ways.
    -d --dry                           Dry run.
    -p --print-all-nodes               Print all available nodes and exit.
    -h --help                          Show this screen.
    --version                          Show version.
```

Output
------
The `miRmachine` main executable will generate GFF annotations (filtered and unfiltered) and some other files.
You will see `results/predictions/` directory which contains:

`gff/` __All predicted miRNA families.__  
`filtered_gff/` __High confidence miRNA family predictions after bitscore filtering.__  
`fasta/` __Both high and low confidence predictions in FASTA format.__  



