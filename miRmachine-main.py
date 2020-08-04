#!/usr/bin/env python
'''
Created on 03/08/2020

miRmachine main

@author: suu13
'''

from __future__ import print_function
import re
from docopt import docopt
import newick
import os
import subprocess
from pathlib import Path

__author__ = 'sium'

__licence__="""
MIT License

Copyright (c) 2020 Sinan Ugur Umu (SUU) sinanugur@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

__doc__="""Main miRmachine executable

Usage:
    miRmachine-main.py --node <text> --species <text> --genome <text> [--model <text>] [--cpu <integer>]
    miRmachine-main.py (-h | --help)
    miRmachine-main.py --version

Arguments:
    -n <text>, --node <text>              Node name. (e.g. Caenorhabditis)
    -s <text>, --species <text>           Species name. (e.g. Caenorhabditis_elegans)
    -g <text>, --genome <text>            Genome fasta file location (e.g. data/genome/example.fasta)
    -m <text>, --model <text>             Model type: deutero, proto, combined [default: proto]
    -c <integer>, --cpu <integer>         CPUs. [default: 2]

Options:
    -h --help                          Show this screen.
    --version                          Show version.

"""


def run_mirmachine():

    Path("data/yamls").mkdir(parents=True,exist_ok=True)

    yaml_argument="""echo {node} | tr "," "\n" | while read i; 
    do bin/miRmachine-tree-parser.py meta/tree.newick $i; done | sort | uniq | while read a; 
    do grep $a meta/nodes_mirnas_corrected.tsv; done | grep -v NOVEL | grep -v NA | cut -f3 | sort | uniq | awk -v genome={genome} -v species={species} -v node={node} 'BEGIN{{print "genome: "genome;print "species: "species;print "node: "node; print "mirnas:"}}{{print " - "$1}}' > data/yamls/{species}.yaml""".format(node=arguments['--node'],species=arguments['--species'],genome=arguments['--genome'])
    
    subprocess.check_call(yaml_argument,shell=True)

    snakemake_argument="snakemake -j {cpu} -s workflows/mirmachine_search.smk --config model={model} --configfile=data/yamls/{species}.yaml".format(species=arguments['--species'],
    cpu=arguments['--cpu'],
    model=arguments['--model'])
    subprocess.call(snakemake_argument,shell=True)

def main():
    run_mirmachine()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.0')
    main()
