# MirMachine

[![Build Status](https://app.travis-ci.com/sinanugur/MirMachine.svg?branch=master)](https://app.travis-ci.com/sinanugur/MirMachine) [![Documentation Status](https://readthedocs.org/projects/mirmachine/badge/?version=latest)](https://mirmachine.readthedocs.io/en/latest/?badge=latest)  


[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)  [![PyPI version](https://badge.fury.io/py/MirMachine.svg?style=flat&cache-control=no-cache)](https://badge.fury.io/py/MirMachine)  [![Anaconda-Server Badge](https://anaconda.org/bioconda/mirmachine/badges/version.svg?style=flat&cache-control=no-cache)](https://anaconda.org/bioconda/mirmachine)  [![Anaconda-Server Badge](https://anaconda.org/bioconda/mirmachine/badges/downloads.svg?style=flat&cache-control=no-cache)](https://anaconda.org/bioconda/mirmachine)  
[![Anaconda-Server Badge](https://anaconda.org/bioconda/mirmachine/badges/latest_release_relative_date.svg?style=flat&cache-control=no-cache)](https://anaconda.org/bioconda/mirmachine)  [![Docker Pulls](https://img.shields.io/docker/pulls/sinanugur/mirmachine)](https://hub.docker.com/r/sinanugur/mirmachine)  
A command line tool to detect miRNA homologs in genome sequences.


Installation
------------
To install this package with conda run:

```
conda install mirmachine -c bioconda -c conda-forge
```

Please add conda-forge as a channel. Installing via [mamba](https://github.com/mamba-org/mamba) is also strongly recommended for a faster installation. You can install __mamba__ and later MirMachine like this:
```
conda install mamba -c conda-forge
mamba install mirmachine -c bioconda -c conda-forge
```

Check if the installation works by calling the main script.  
```
MirMachine.py --help
```

Note: You have to install dependencies if you prefer GitHub or PyPi installation.

Quick start example
-------------------
Create a new directory and run MirMachine there after the installation. MirMachine will create the required directories while running.
```
MirMachine.py -n Caenorhabditis -s Caenorhabditis_elegans --genome sample/genomes/ce11.fa --cpu 20 --model proto
```

See our documentation for detailed explanations: https://mirmachine.readthedocs.io/

Options and Arguments
---------------------
```
Usage:
    MirMachine.py --node <text> --species <text> --genome <text> [--model <text>] [--evalue <float>] [--cpu <integer>] [--add-all-nodes|--single-node-only] [--unlock|--remove][--touch] [--dry]
    MirMachine.py --species <text> --genome <text> --family <text> [--model <text>] [--evalue <float>] [--cpu <integer>] [--unlock|--remove] [--touch] [--dry]
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
    -e <text>, --evalue <float>           Inclusion E-value. May inflate low quality hits. [default: 0.2]
    -c <integer>, --cpu <integer>         CPUs. [default: 2]

Options:
    -a, --add-all-nodes                 Move on the tree both ways. NOT required most of the time.
    -o, --single-node-only              Run only on the given node for miRNA families.
    -p, --print-all-nodes               Print all available node options and exit.
    -l, --print-all-families            Print all available families in this version and exit.
    -t, --print-ascii-tree              Print ascii tree of the tree file.
    -u, --unlock                        Rescue stalled jobs (Try this if the previous job ended prematurely).
    -r, --remove                        Clear all output files (this won't remove input files).
    -d, --dry                           Dry run.
    -h, --help                          Show this screen.
    --touch                             Touch output files (mark them up to date without really changing them).
    --version                           Show version.
```

Output
------
The `MirMachine` main executable will generate GFF annotations (filtered and unfiltered) and some other files.
You will see `results/predictions/` directory which contains:

`gff/` __All predicted miRNA families.__  
`filtered_gff/` __High confidence miRNA family predictions after bitscore filtering. (This file is what you need in most cases)__  
`fasta/` __Both high and low confidence predictions in FASTA format.__  


MirMachine's other repos
------
Web application repo: https://github.com/selfjell/MirMachine  
Supplementary files repo: https://github.com/sinanugur/MirMachine-supplementary

Citiation
------
Our Cell Genomics paper is here: [https://doi.org/10.1016/j.xgen.2023.100348](https://doi.org/10.1016/j.xgen.2023.100348)
Please cite if you find our tool useful.


