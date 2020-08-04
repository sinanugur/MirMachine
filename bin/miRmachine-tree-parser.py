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
    miRmachine-tree-parser.py <newick> <keyword>
    miRmachine-tree-parser.py (-h | --help)
    miRmachine-tree-parser.py --version

Arguments:
    newick                              A newick tree.
    keyword                             A keyword to gather node miRNAs (e.g. Homo).

Options:
    -h --help                          Show this screen.
    --version                          Show version.

"""


def detect_ancestors(node,ancestors):
    if node == None:
        return
    else:
        if node.name != None:
            ancestors.extend([x.strip() for x in node.name.split("_")])
        detect_ancestors(node.ancestor,ancestors)

def search_tree_for_keyword(newick_file,keyword):

    ancestors=list()
    tree=newick.read(newick_file)
    for node in tree[0].walk():
        if node.name is not None and node.name.find(keyword.strip()) != -1:
            detect_ancestors(node, ancestors)

            for i in ancestors:
                print(i)

            break

    return






def main():
    search_tree_for_keyword(arguments['<newick>'],arguments['<keyword>'])


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.95')
    main()
