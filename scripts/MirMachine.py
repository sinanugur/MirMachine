#!/usr/bin/env python
'''
Created on 03/08/2020

MirMachine main

@author: suu13
'''

#from __future__ import print_function
import re
from docopt import docopt
import newick
import os
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from mirmachine import meta
    from mirmachine import workflows
    import mirmachine
    mirmachine_path=os.path.dirname(mirmachine.__file__)
except ImportError:
    try:
        import meta
        import workflows
        mirmachine_path="mirmachine" #so you did not install the package
    except:
            raise ImportError


meta_directory=os.path.dirname(meta.__file__)

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

__doc__="""Main MirMachine executable

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

"""




def run_mirmachine():

    Path("data/yamls").mkdir(parents=True,exist_ok=True)

    both_ways= "--add-all-nodes" if arguments["--add-all-nodes"] else ""
    dry_run="-n" if arguments["--dry"] else ""

    yaml_argument="""echo {node} | tr "," "\n" | while read i; 
    do mirmachine-tree-parser.py {meta_directory}/tree.newick $i {both_ways}; done | sort | uniq | while read a; \
    do grep $a {meta_directory}/nodes_mirnas_corrected.tsv; done \
     | grep -v NOVEL | grep -v NA | cut -f3 | sort | uniq | \
      awk -v genome={genome} -v species={species} -v node={node} 'BEGIN{{print "genome: "genome;print "species: "species;print "node: "node; print "mirnas:"}}{{print " - "$1}}' > data/yamls/{species}.yaml""".format(
          node=arguments['--node'],
          both_ways=both_ways,
          mirmachine_path=mirmachine_path,
          meta_directory=meta_directory,
          species=arguments['--species'],
          genome=arguments['--genome'])
    
    subprocess.check_call(yaml_argument,shell=True)

    snakemake_argument="snakemake {dry} -j {cpu} -s {mirmachine_path}/workflows/mirmachine_search.smk --config meta_directory={meta_directory} model={model} mirmachine_path={mirmachine_path} --configfile=data/yamls/{species}.yaml".format(
    species=arguments['--species'],
    cpu=arguments['--cpu'],
    model=arguments['--model'],
    meta_directory=meta_directory,
    mirmachine_path=mirmachine_path,
    dry=dry_run)
    
    subprocess.call(snakemake_argument,shell=True)

def main():
    if arguments["--print-all-nodes"]:
        tree_parser_argument="mirmachine-tree-parser.py {meta_directory}/tree.newick --print-all-nodes".format(meta_directory=meta_directory,mirmachine_path=mirmachine_path)
        subprocess.call(tree_parser_argument,shell=True)
    else:
        start_time = datetime.now()
        run_mirmachine()
        end_time = datetime.now()
        print('Total runtime: {}'.format(end_time - start_time))


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.2')
    main()
