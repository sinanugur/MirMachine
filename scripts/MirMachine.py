#!/usr/bin/env python
'''
Created on 03/08/2020

MirMachine main

@author: Sinan U. Umu, sinanugur@gmail.com
'''

#from __future__ import print_function
import re
import os
import shutil
import sys
import subprocess
from pathlib import Path
from datetime import datetime

import newick
import yaml
from docopt import docopt
#from schema import Schema, And, Or, Use, SchemaError

from rich.console import Console
from rich.columns import Columns
from rich import print
from rich.panel import Panel

from collections import defaultdict

try:
    from mirmachine import meta
    import mirmachine
    mirmachine_path=os.path.dirname(mirmachine.__file__)
except ImportError:
    try:
        import meta
        mirmachine_path="mirmachine" #so you did not install the package
    except:
            raise ImportError


meta_directory=os.path.dirname(meta.__file__)
tree_file=os.path.join(meta_directory, "tree.newick")
nodes_mirnas_file=os.path.join(meta_directory, "nodes_mirnas_corrected.tsv")
losses_mirnas_file=os.path.join(meta_directory, "losses_mirnas.tsv")

__author__ = 'sium'
__version__= '0.3.0.4b'


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
    MirMachine.py --node <text> --species <text> --genome <text> [--model <text>] [--evalue <float>] [--cpu <integer>] [--add-all-nodes|--single-node-only] [--unlock|--remove] [--touch] [--dry] [--long]
    MirMachine.py --species <text> --genome <text> --family <text> [--model <text>] [--evalue <float>] [--cpu <integer>] [--unlock|--remove] [--touch] [--dry] [--long]
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
    --long                              Use long miRNA covariance models rather than standard models (Experimental).
    -p, --print-all-nodes               Print all available node options and exit.
    -l, --print-all-families            Print all available families in this version and exit.
    -t, --print-ascii-tree              Print ascii tree of the tree file.
    -u, --unlock                        Rescue stalled jobs (Try this if the previous job ended prematurely).
    -r, --remove                        Clear all output files (this won't remove input files).
    -d, --dry                           Dry run.
    -h, --help                          Show this screen.
    --touch                             Touch output files (mark them up to date without really changing them).
    --version                           Show version.

"""


def _resolve_cm_directory(use_long_models=False):
    cm_subdir = "lcms" if use_long_models else "cms"
    return os.path.join(meta_directory, cm_subdir)

def _split_node_name(name):
    if name is None:
        return []
    return [part.strip() for part in name.split("_") if part.strip()]


def _walk_tree_nodes(newick_path):
    descendants = []
    tree = newick.read(newick_path)
    for node in tree[0].walk():
        if node.name is not None and not node.is_leaf: #I skip leaf nodes.
            descendants.extend(
                [label for label in _split_node_name(node.name) if len(label) > 2]
            )

    while "group" in descendants:
        descendants.remove("group")

    pattern = re.compile("[A-Z][a-z]+")
    return list(filter(pattern.match, descendants))


def _detect_ancestors(node, ancestors):
    if node is None:
        return
    if node.name is not None:
        ancestors.extend(_split_node_name(node.name))
    _detect_ancestors(node.ancestor, ancestors)


def _detect_descendants(nodes, descendants):
    if not nodes:
        return
    for node in nodes:
        if node.name is not None and not node.is_leaf: #I skip leaf nodes.
            descendants.extend(_split_node_name(node.name))
        _detect_descendants(node.descendants, descendants)


def _search_tree_for_keyword(newick_path, keyword, include_descendants=False):
    ancestors = []
    descendants = []
    tree = newick.read(newick_path)
    keyword_title = keyword.strip().title()
    for node in tree[0].walk():
        if node.name is not None and re.search(keyword_title, node.name):
            _detect_ancestors(node, ancestors)
            _detect_descendants([node], descendants)
            while "group" in descendants:
                descendants.remove("group")
            while "group" in ancestors:
                ancestors.remove("group")

            if include_descendants:
                return descendants + ancestors
            return ancestors
    return []


def _resolve_nodes_for_query(node_name, include_descendants=False):
    nodes = _search_tree_for_keyword(
        newick_path=tree_file,
        keyword=node_name,
        include_descendants=include_descendants,
    )
    return sorted({node for node in nodes if len(node) > 2})


def _collect_families_from_tsv(tsv_path, nodes):
    valid_nodes = {node for node in nodes if len(node) > 2}
    if not valid_nodes:
        return []

    families = set()
    with open(tsv_path) as tsv:
        for line in tsv:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            node_name, family = parts[0], parts[1].strip()
            if family in {"NOVEL", "NA"}:
                continue
            # Preserve previous grep-like behavior: substring matching on node names.
            if any(node in node_name for node in valid_nodes):
                families.add(family)
    return sorted(families)


def _yaml_output_path(species):
    Path("data/yamls").mkdir(parents=True, exist_ok=True)
    return Path("data/yamls") / f"{species}.yaml"


def _write_yaml_file(path, payload):
    with path.open("w", encoding="utf-8") as yaml_handle:
        yaml.safe_dump(payload, yaml_handle, sort_keys=False, default_flow_style=False)


def print_ascii_tree():
    tree = newick.read(tree_file)[0]
    print(tree.ascii_art())

def print_all_nodes():
    nodes = _walk_tree_nodes(tree_file)
    nodes.sort()
    columns = Columns(nodes, equal=True, expand=True)
    print("All available nodes (leaf node names excluded):")
    print(columns)

def show_node_families():
    node_candidates = _resolve_nodes_for_query(
        node_name=arguments["--node"],
        include_descendants=arguments["--add-all-nodes"],
    )
    families = _collect_families_from_tsv(nodes_mirnas_file, node_candidates)
    families.sort()
    columns = Columns(families, equal=True, expand=True)
    print("All available families of {node} node ".format(node=arguments['--node']))
    print(columns)

def create_yaml_file():
    yaml_path = _yaml_output_path(arguments["--species"])

    payload = {
        "genome": arguments["--genome"],
        "species": arguments["--species"],
        "node": arguments["--node"] or "",
    }

    if arguments["--family"]:
        payload["mirnas"] = [arguments["--family"]]
        _write_yaml_file(yaml_path, payload)
        return

    if arguments["--single-node-only"]:
        query_nodes = [arguments["--node"]]
        loss_nodes = [arguments["--node"]]
    else:
        query_nodes = _resolve_nodes_for_query(
            node_name=arguments["--node"],
            include_descendants=arguments["--add-all-nodes"],
        )
        loss_nodes = _resolve_nodes_for_query(
            node_name=arguments["--node"],
            include_descendants=False,
        )

    payload["mirnas"] = _collect_families_from_tsv(nodes_mirnas_file, query_nodes)
    losses = _collect_families_from_tsv(losses_mirnas_file, loss_nodes)
    if losses:
        payload["losses"] = losses

    _write_yaml_file(yaml_path, payload)

def validate_inputs():

    snakemake_argument = [
        "snakemake",
        "-j",
        str(arguments["--cpu"]),
        "-s",
        f"{mirmachine_path}/workflows/test.smk",
        "--config",
        f"meta_directory={meta_directory}",
        f"cm_directory={_resolve_cm_directory(arguments['--long'])}",
        f"nonull3={"Yes" if arguments['--long'] else "No"}",
        f"model={arguments['--model'].lower()}",
        f"mirmachine_path={mirmachine_path}",
        "--configfile",
        str(_yaml_output_path(arguments["--species"])),
    ]
    subprocess.run(
        snakemake_argument,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    

def print_available_families():
    
    console = Console()
    #table = Table(show_header=True, header_style="bold magenta")
    dct=defaultdict(list)

    

    for model in ["combined","deutero", "proto"]:
        cutoff_file=meta_directory + "/cutoffs/" + model + "/mirmachine_trusted_cutoffs.tsv"
        

        #table.add_column(model)
        
        
        
        #print("{model} families:".format(model=model))
        with open(cutoff_file) as tsv:
            for line in tsv.readlines():
                #print(line.split()[0])
                dct[model].append(line.split()[0])
        dct[model].sort()
        columns = Columns(dct[model], equal=True, expand=True)
        console.print("[bold]All available families in {model} model. [/bold]".format(model=model))
        print(columns)
    return


def run_mirmachine():

    snakemake_argument = ["snakemake", "-q", "rules", "--rerun-incomplete"]
    if arguments["--touch"]:
        snakemake_argument.append("--touch")
    if arguments["--dry"]:
        snakemake_argument.append("-n")
    if arguments["--unlock"]:
        snakemake_argument.append("--unlock")
    if arguments["--remove"]:
        snakemake_argument.append("--delete-all-output")

    snakemake_argument.extend(
        [
            "-j",
            str(arguments["--cpu"]),
            "-s",
            f"{mirmachine_path}/workflows/mirmachine_search.smk",
            "--config",
            f"meta_directory={meta_directory}",
            f"cm_directory={_resolve_cm_directory(arguments['--long'])}",
            f"model={arguments['--model'].lower()}",
            f"evalue={arguments['--evalue']}",
            f"params={' '.join(sys.argv)}",
            f"mirmachine_path={mirmachine_path}",
            "--configfile",
            str(_yaml_output_path(arguments["--species"])),
        ]
    )
    subprocess.run(snakemake_argument, check=True)


def clean_meta_directory():
    # delete .snakemake directory
    shutil.rmtree(".snakemake", ignore_errors=True)


def _parse_headers(path):
    parsed_data = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or not line.startswith("#"):
                continue

            stripped = line.lstrip("#").strip()
            if ":" in stripped:
                key, value = stripped.split(":", 1)
                parsed_data[key.strip()] = value.strip()
            else:
                parts = stripped.split(None, 1)
                if len(parts) == 2:
                    key, value = parts
                    parsed_data[key] = value
    return parsed_data

def print_gff_header(filename):
    filtered_file = Path("results/predictions/filtered_gff") / filename
    unfiltered_file = Path("results/predictions/gff") / filename

    for key, value in _parse_headers(filtered_file).items():
        line = f"{key}: {value}"
        if "searched" in line or "losses" in line:
            continue
        print(line)

    for key, value in _parse_headers(unfiltered_file).items():
        line = f"{key}: {value}"
        if "score" in line:
            print(line.replace("score", "unfiltered score"))

def main():
    parsed_tree=_walk_tree_nodes(tree_file)

    #if arguments["--print-all-nodes"]:
    #    if arguments["--node"].title() in parsed_tree:
    #        print_all_nodes()
    if arguments["--print-ascii-tree"]:
        print_ascii_tree()
    elif arguments["--print-all-families"]:
        print_available_families()
    elif not arguments["--species"] and not arguments["--genome"] and arguments["--node"] and arguments["--node"].title() in parsed_tree:
        show_node_families()
    else:
        if arguments["--node"] and arguments["--node"].title() not in parsed_tree and arguments["--family"] is None:

            print(Panel.fit("""Error, the node name argument is wrong!\nThe node name given is: "{node}"\nPlease select one of the following:""".format(node=arguments["--node"])))
            print_all_nodes()
            return
        elif arguments["--print-all-nodes"]:
            print_all_nodes()
            return


        start_time = datetime.now()
        create_yaml_file()

        if arguments["--model"].lower() not in ["deutero", "proto", "combined"]:
            print(Panel.fit("""Error, please select a correct model name!"\nThe model given is: "{model}"\nPossible values are: "deutero", "proto", "combined" """.format(model=arguments["--model"])))
            return
        try:
            #validate_inputs()
            pass
        except:
            #print(Panel.fit("""Error, model and node names are inconsistent!\nThe model given is: "{model}"\nThe node name given is: "{node}"\nChanging to the default model: combined""".format(model=arguments["--model"],node=arguments["--node"])))
            #arguments["--model"]="combined"
            pass
            try:
                #validate_inputs()
                pass
            except:
                print("")
                print("Error, miRNA family not found.")
                console = Console()
                console.print("You can run [bold red]MirMachine.py --print-all-families [/bold red] to see available families")
                return

        if not os.path.isfile(arguments["--genome"]):
            print(Panel.fit("""Error, the genome file does not exist!\nThe genome file given is: "{genome}"\nPlease select a correct genome file in uncompressed FASTA format.""".format(genome=arguments["--genome"])))
            return

        run_mirmachine()
        end_time = datetime.now()
        print('Total runtime: {}'.format(end_time - start_time))
        print("MirMachine run completed. Cleaning up .snakemake directory...")
        try:
            if os.path.isdir(".snakemake"):
                clean_meta_directory()

            filename=f"{arguments['--species']}.PRE.gff"
            if os.path.exists("results/predictions/filtered_gff/" + filename) and not arguments["--dry"]:
                print_gff_header(filename)
                
        except:
            pass



if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    main()
