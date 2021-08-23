#!/usr/bin/env python
'''
Created on 16/04/2018

miRmachine walk on tree, parse out node miRNAs


@author: suu13
'''

from __future__ import print_function
import re
from docopt import docopt
import newick


__author__ = 'sium'

__licence__="""
MIT License

Copyright (c) 2018 Sinan Ugur Umu (SUU) sinanugur@gmail.com

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

__doc__="""Parse tree to find node miRNAs.

Usage:
    mirmachine-tree-parser.py <newick> <keyword> [--add-all-nodes]
    mirmachine-tree-parser.py <newick> --print-all-nodes
    mirmachine-tree-parser.py <newick> --print-ascii-tree
    mirmachine-tree-parser.py (-h | --help)
    mirmachine-tree-parser.py --version

Arguments:
    newick                              A newick tree.
    keyword                             A keyword to gather node miRNAs (e.g. Homo).

Options:
    -a --add-all-nodes                 Move on the tree both ways.
    -p --print-all-nodes               Print all available nodes and exit.
    -pa --print-ascii-tree             Print ascii tree of the tree file.
    -h --help                          Show this screen.
    --version                          Show version.

"""


def detect_ancestors(node,ancestors):
    if node == None:
        return
    else:
        if node.name is not None:
            ancestors.extend([x.strip() for x in node.name.split("_")])
        detect_ancestors(node.ancestor,ancestors)

    return

def detect_descendants(node,descendants):
    if not node:
        return
    else:
        for i in node:
            if i.name is not None and not i.is_leaf: #I skip leaf nodes.
                descendants.extend([x.strip() for x in i.name.split("_")])
            detect_descendants(i.descendants,descendants)

    return

def walk_on_tree(newick_file):
    descendants=[]
    tree=newick.read(newick_file)
    for node in tree[0].walk():
        if node.name is not None and not node.is_leaf: #I skip leaf nodes.
            y=[x.strip() for x in node.name.split("_")]
            descendants.extend(list(filter(lambda x: len(x) > 2,y)))
    
    while "group" in descendants: descendants.remove("group") 

    r=re.compile("[A-Z][a-z]+")

    for d in list(filter(r.match,descendants)):
        print(d)

    return



def search_tree_for_keyword(newick_file,keyword):

    ancestors=[]
    descendants=[]
    tree=newick.read(newick_file)
    for node in tree[0].walk():
        #if node.name is not None and node.name.find(keyword.strip()) != -1:
        if node.name is not None and re.search(keyword.strip().title(),node.name):
            detect_ancestors(node, ancestors)
            detect_descendants([node], descendants)
            while "group" in descendants: descendants.remove("group") 
            while "group" in ancestors: ancestors.remove("group") 
            
            if arguments['--add-all-nodes']:
                for d in descendants:
                    print(d)
            for a in ancestors:
                print(a)

            break

    return



def print_tree(newick_file):
    tree=newick.read(newick_file)[0]
    print(tree.ascii_art())


def main():
    if arguments["--print-all-nodes"]:
        walk_on_tree(arguments['<newick>'])
    elif arguments["--print-ascii-tree"]:
        print_tree(arguments['<newick>'])
    else:
        search_tree_for_keyword(arguments['<newick>'],arguments['<keyword>'])


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.98')
    main()
