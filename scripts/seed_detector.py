#!/usr/bin/env python
'''
Created on 01/02/2024

Seed detector

@author: suu13
'''


import sys
from Bio import SeqIO
import ast

def check_patterns(patterns, target_sequence):
    p=[]
    for pattern in patterns:
        if pattern.strip() in target_sequence:
            p.append(pattern)
    return p

def read_fasta(file_path):
    sequences = {}

    for record in SeqIO.parse(file_path, "fasta"):
        header = str(record.id)
        sequence = str(record.seq)
        sequences[header] = sequence

    return sequences

def modify_header(sequence_dict):
    modified_sequences = {}

    for header, sequence in sequence_dict.items():
        sequence=sequence.upper().replace('U','T')

        p5 = check_patterns(patterns_5p, sequence[:10].upper())

        p3 = check_patterns(patterns_3p, sequence[-28:][:16].upper())

        if not p3 and not p5: 
            modified_sequences[header] = sequence
        else:
            new_header=header
            if p5:
                new_header = "{new_header}_p5_seed({p5})".format(new_header=new_header, p5=','.join(p5))
            if p3:
                new_header = "{new_header}_p3_seed({p3})".format(new_header=new_header, p3=','.join(p3))
            modified_sequences[new_header] = sequence

    return modified_sequences


def write_fasta(sequence_dict):
    
    for header, sequence in sequence_dict.items():
        print(f'>{header}\n{sequence}')

def main():
    sequences = read_fasta(sys.argv[1])
    modified_sequences = modify_header(sequences)
    #write_fasta(output_file_path, modified_sequences)
    write_fasta(modified_sequences)





if __name__ == '__main__':
    try:
        #patterns_5p = ast.literal_eval(sys.argv[2])
        patterns_5p = sys.argv[2].split()
    except:
        patterns_5p = []

    try:
        #patterns_3p = ast.literal_eval(sys.argv[3])
        patterns_3p = sys.argv[3].split()
    except:
        patterns_3p = []
    main()    
