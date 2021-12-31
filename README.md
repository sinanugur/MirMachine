# MirMachine

[![Build Status](https://app.travis-ci.com/sinanugur/MirMachine.svg?branch=master)](https://app.travis-ci.com/sinanugur/MirMachine)  

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)  [![PyPI version](https://badge.fury.io/py/MirMachine.svg)](https://badge.fury.io/py/MirMachine)  [![Anaconda-Server Badge](https://anaconda.org/bioconda/mirmachine/badges/installer/conda.svg)](https://conda.anaconda.org/bioconda)  [![Anaconda-Server Badge](https://anaconda.org/bioconda/mirmachine/badges/downloads.svg)](https://anaconda.org/bioconda/mirmachine)  
[![Anaconda-Server Badge](https://anaconda.org/bioconda/mirmachine/badges/latest_release_relative_date.svg)](https://anaconda.org/bioconda/mirmachine)  
A command line tool to detect miRNA homologs in genome sequences.


Installation
------------
To install this package with conda run:

```
conda install -c bioconda -c conda-forge mirmachine
```

Please add conda-forge as a channel.  

Alternative method for installing dev version:
```
git clone https://github.com/sinanugur/MirMachine.git
cd MirMachine
pip install .
```

Check if the installation works by calling the main script.  
```
MirMachine.py --help
```

You have to install dependencies via conda if you prefer Github installation.  

Quick start example
-------------------
Create a new directory and run MirMachine there after the installation. MirMachine will create the required directories while running.
```
MirMachine.py -n Caenorhabditis -s Caenorhabditis_elegans --genome sample/genomes/ce11.fa --cpu 20
```

Options and Arguments
---------------------
```
Usage:
    MirMachine.py --node <text> --species <text> --genome <text> [--model <text>] [--cpu <integer>] [--add-all-nodes|--single-node-only] [--unlock|--remove] [--dry]
    MirMachine.py --species <text> --genome <text> --family <text> [--model <text>] [--unlock|--remove] [--dry]
    MirMachine.py --node <text> [--add-all-nodes]
    MirMachine.py --print-all-nodes
    MirMachine.py --print-all-families
    MirMachine.py --print-ascii-tree
    MirMachine.py (-h | --help)
    MirMachine.py --version

Arguments:
    -n <text>, --node <text>              Node name. (e.g. Caenorhabditis)
    -s <text>, --species <text>           Species name. (e.g. Caenorhabditis_elegans)
    -g <text>, --genome <text>            Genome fasta file location (e.g. data/genome/example.fasta)
    -m <text>, --model <text>             Model type: deutero, proto, combined [default: combined]
    -f <text>, --family <text>            Run only a single miRNA family (e.g. Let-7).
    -c <integer>, --cpu <integer>         CPUs. [default: 2]

Options:
    -a, --add-all-nodes                 Move on the tree both ways.
    -o, --single-node-only              Run only on the given node for miRNA families.
    -p, --print-all-nodes               Print all available node options and exit.
    -l, --print-all-families            Print all available families in this version and exit.
    -t, --print-ascii-tree              Print ascii tree of the tree file.
    -u, --unlock                        Rescue stalled jobs (Try this if the previous job ended prematurely).
    -r, --remove                        Clear all output files (this won't remove input files).
    -d, --dry                           Dry run.
    -h, --help                          Show this screen.
    --version                           Show version.
```

Output
------
The `MirMachine` main executable will generate GFF annotations (filtered and unfiltered) and some other files.
You will see `results/predictions/` directory which contains:

`gff/` __All predicted miRNA families.__  
`filtered_gff/` __High confidence miRNA family predictions after bitscore filtering. (This file is what you need in most cases)__  
`fasta/` __Both high and low confidence predictions in FASTA format.__  



