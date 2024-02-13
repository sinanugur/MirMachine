#!/usr/bin/env python
'''
Created on 01/02/2024

Seed detector

@author: suu13
'''


import sys
import ast

def check_patterns(patterns, target_sequence):
    for pattern in patterns:
        if pattern in target_sequence:
            return pattern
    return None

def read_fasta(file_path):
    sequences = {}
    current_header = None
    current_sequence = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                # If it's a header line
                if current_header is not None:
                    # Store the previous sequence
                    sequences[current_header] = ''.join(current_sequence)
                
                # Update the current header
                current_header = line[1:]
                current_sequence = []
            else:
                # If it's a sequence line
                current_sequence.append(line)

        # Store the last sequence
        if current_header is not None:
            sequences[current_header] = ''.join(current_sequence)

    return sequences

def modify_header(sequence_dict):
    modified_sequences = {}

    for header, sequence in sequence_dict.items():
        sequence=sequence.upper().replace('U','T')

        p5 = check_patterns(patterns_5p, sequence[:10].upper())

        p3 = check_patterns(patterns_3p, sequence[-28:][:16].upper())

        if p3 is None and p5 is None: 
            modified_sequences[header] = sequence
        else:
            if p5 is not None:
                new_header = f"{header}_p5_seed({p5})" 
                modified_sequences[new_header] = sequence
            if p3 is not None:
                new_header = f"{header}_p3_seed({p3})"
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
