# MirMachine

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)  [![PyPI version](https://badge.fury.io/py/MirMachine.svg)](https://badge.fury.io/py/MirMachine)  
A command line to tool detect miRNA homologs in genome sequences.  

Installation
------------
To create required environment using Anaconda:

```
conda env create -f environment.yml
conda activate mirmachine
```

Then install from Pypi:
```
pip install mirmachine
```

Alternative method:
```
git clone https://github.com/sinanugur/MirMachine.git
cd MirMachine
pip install .
```

Check if the installation works by calling the main script.
```
MirMachine.py
```

Quick start example
-------------------
Create a new directory and run MirMachine there after the installation. MirMachine will create the required directories while running.
```
MirMachine.py -n Caenorhabditis -s Caenorhabditis_elegans --genome data/genomes/ce11.fasta -m proto --cpu 20
```

Options and Arguments
---------------------
```
Usage:
    MirMachine.py --node <text> --species <text> --genome <text> [--model <text>] [--cpu <integer>] [--add-all-nodes] [--dry]
    MirMachine.py --print-all-nodes
    MirMachine.py (-h | --help)
    MirMachine.py --version

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
The `MirMachine` main executable will generate GFF annotations (filtered and unfiltered) and some other files.
You will see `results/predictions/` directory which contains:

`gff/` __All predicted miRNA families.__  
`filtered_gff/` __High confidence miRNA family predictions after bitscore filtering.__  
`fasta/` __Both high and low confidence predictions in FASTA format.__  



