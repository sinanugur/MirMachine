#!/usr/bin/env python
'''
Created on 03/08/2020

MirMachine main

@author: Sinan U. Umu, sinanugur@gmail.com
'''

#from __future__ import print_function
import re
from docopt import docopt
import newick
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
#from schema import Schema, And, Or, Use, SchemaError

from rich.console import Console
from rich.table import Column, Table
from rich.columns import Columns
from rich import print

import importlib
from collections import defaultdict

walk_on_tree=importlib.import_module("mirmachine-tree-parser")

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
__version__= '0.2.11.2'


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

"""

def print_ascii_tree():
    tree_parser_argument="mirmachine-tree-parser.py {meta_directory}/tree.newick --print-ascii-tree".format(meta_directory=meta_directory)
    subprocess.check_call(tree_parser_argument,shell=True)

def print_all_nodes():
    tree_parser_argument="mirmachine-tree-parser.py {meta_directory}/tree.newick --print-all-nodes".format(meta_directory=meta_directory)
    print("All available nodes (leaf node names excluded):")
    all_nodes=subprocess.check_output(tree_parser_argument,shell=True).splitlines()
    #all_nodes=all_nodes.split("\n")
    print(all_nodes)

def show_node_families():
    both_ways= "--add-all-nodes" if arguments["--add-all-nodes"] else ""
    yaml_argument="""echo {node} | while read i; do mirmachine-tree-parser.py {meta_directory}/tree.newick $i {both_ways}; done | sort | uniq | while read a; \
        do grep $a {meta_directory}/nodes_mirnas_corrected.tsv; done \
        | grep -v NOVEL | grep -v NA | cut -f2 | sort | uniq""".format(node=arguments['--node'],meta_directory=meta_directory,both_ways=both_ways)

    subprocess.check_call(yaml_argument,shell=True)

def create_yaml_file():
    Path("data/yamls").mkdir(parents=True,exist_ok=True)

    both_ways= "--add-all-nodes" if arguments["--add-all-nodes"] else ""
    default_node_argument= "" if arguments["--single-node-only"] else "| while read i; do mirmachine-tree-parser.py {meta_directory}/tree.newick $i {both_ways}; done".format(meta_directory=meta_directory,both_ways=both_ways)

    if arguments['--family']:
        yaml_argument = """echo {family} | awk -v genome={genome} -v species={species} 'BEGIN{{print "genome: "genome;print "species: "species;print "node: "node; print "mirnas:"}}{{print " - "$1}}' > data/yamls/{species}.yaml""".format(
        family=arguments['--family'],
          species=arguments['--species'],
          genome=arguments['--genome'])
    
    else:
        yaml_argument="""echo {node} {default_node_argument} | sort | uniq | while read a; \
        do grep $a {meta_directory}/nodes_mirnas_corrected.tsv; done \
        | grep -v NOVEL | grep -v NA | cut -f2 | sort | uniq | \
        awk -v genome={genome} -v species={species} -v node={node} 'BEGIN{{print "genome: "genome;print "species: "species;print "node: "node; print "mirnas:"}}{{print " - "$1}}' > data/yamls/{species}.yaml""".format(
          default_node_argument=default_node_argument,
          meta_directory=meta_directory,
          node=arguments['--node'],
            mirmachine_path=mirmachine_path,
          species=arguments['--species'],
          genome=arguments['--genome'])

    subprocess.check_call(yaml_argument,shell=True)



def validate_inputs():

    snakemake_argument="snakemake -j {cpu} -s {mirmachine_path}/workflows/test.smk --config meta_directory={meta_directory} model={model} mirmachine_path={mirmachine_path} --configfile=data/yamls/{species}.yaml".format(
    species=arguments['--species'],
    cpu=arguments['--cpu'],
    model=arguments['--model'].lower(),
    meta_directory=meta_directory,
    mirmachine_path=mirmachine_path  
    )

    subprocess.check_call(snakemake_argument,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    

def print_available_families():
    
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    dct=defaultdict(list)

    for model in ["combined","deutero", "proto"]:
        cutoff_file=meta_directory + "/cutoffs/" + model + "/mirmachine_trusted_cutoffs.tsv"
        

        table.add_column(model)
        
        
        
        #print("{model} families:".format(model=model))
        with open(cutoff_file) as tsv:
            for line in tsv.readlines():
                #print(line.split()[0])
                dct[model].append(line.split()[0])
                
    dct["combined"].sort()
    dct["deutero"].sort()
    dct["proto"].sort()

    for i in range(0,len(dct["combined"])):
        crow=dct["combined"][i]
        try:
            drow=dct["deutero"][i]
        except:
            drow=""
        try:
            prow=dct["proto"][i]
        except:
            prow=""
        
        table.add_row(crow,drow,prow)
        
    console.print(table)
        
    return




def run_mirmachine():

    params="'{p}'".format(p=" ".join(sys.argv))
    dry_run="-n" if arguments["--dry"] else ""
    unlock="--unlock" if arguments["--unlock"] else ""
    remove="--delete-all-output" if arguments["--remove"] else ""
    snakemake_argument="snakemake --rerun-incomplete {dry} {unlock} {remove} -j {cpu} -s {mirmachine_path}/workflows/mirmachine_search.smk --config meta_directory={meta_directory} model={model} params={params} mirmachine_path={mirmachine_path} --configfile=data/yamls/{species}.yaml".format(
    species=arguments['--species'],
    cpu=arguments['--cpu'],
    model=arguments['--model'].lower(),
    meta_directory=meta_directory,
    mirmachine_path=mirmachine_path,
    dry=dry_run,
    unlock=unlock,
    remove=remove,
    params=params)
    
    subprocess.check_call(snakemake_argument,shell=True)




def main():
    if arguments["--print-all-nodes"]:
        print_all_nodes()
    elif arguments["--print-ascii-tree"]:
        print_ascii_tree()
    elif arguments["--print-all-families"]:
        print_available_families()
    elif not arguments["--species"] and not arguments["--genome"]:
        show_node_families()
    else:
        start_time = datetime.now()
        create_yaml_file()
        parsed_tree=walk_on_tree.walk_on_tree("{meta_directory}/tree.newick".format(meta_directory=meta_directory))       
        if arguments["--node"] is not None and arguments["--node"].title() not in parsed_tree and arguments["--family"] is not None:
            print("Error, the node name argument is wrong !")
            print("""The node name given is: "{node}" """.format(node=arguments["--node"]))
            print("Please select one of the following: ")
            print("")
            print(parsed_tree)
            return

        if arguments["--model"].lower() not in ["deutero", "proto", "combined"]:
            print("Error, please select a correct model name !")
            print("""The model given is: "{model}" """.format(model=arguments["--model"]))
            print("""Possible values are: "deutero", "proto", "combined" """)
            return
        try:
            validate_inputs()
        except:
            print("Error, model and node names are inconsistent.")
            print("""The model given is: "{model}" """.format(model=arguments["--model"]))
            print("""The node name given is: "{node}" """.format(node=arguments["--node"]))
            print("Changing to the default model: combined")
            
            arguments["--model"]="combined"
            try:
                validate_inputs()
            except:
                print("")
                print("Error, miRNA family not found.")
                console = Console()
                console.print("You can run [bold red]MirMachine.py --print-all-families [/bold red] to see available families")
                return



        run_mirmachine()
        end_time = datetime.now()
        print('Total runtime: {}'.format(end_time - start_time))


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    main()
