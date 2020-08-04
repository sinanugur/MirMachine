#!/bin/bash

# remove_duplicate_sequence.shx is a short bash to remove multiple copies of sequences from an input fasta file and saves the result in an output fasta file.
# the bash script was based on Pierre Lindenbaum's script: https://www.biostars.org/p/3003/#3008
# input:
# -f | --file  : fasta file
# -o | --output : output file after removing all the sequences
#
while [ "$1" != "" ]; do
	        case $1 in
			                -f | --file ) shift
						                        fileName=$1
									                        ;;
												                -o | --output ) shift
															                        outputFile=$1
																		                        ;;
																					                * ) exit 1
																								        esac
																									        shift
																									done
																									# The following pipline is composed of the following actions:
																									# in every row that starts with '>' put '@' at the end of the row
																									# replace '>' with '#'
																									# remove the break lines, replace '#' with a breakline, replace '@' with a tab
																									# sort the file according to the second column (sequences). the -u option keeps only one copy of each unique string.
																									# add '>' at the begining of each line
																									# sustitute tab (\t)  with a breakline (\n)
																									# remove the first line (it's a blank line) and save the result into $output

																									        sed '/^>/s/$/@/' < $fileName |
																										        sed 's/^>/#/' |\
																												        tr -d '\n' | tr "#" "\n" | tr "@" "\t" |\
																													        sort -u -f -k 2,2  |\
																														        sed -e 's/^/>/' |\
																															        tr '\t' '\n/' |\
																																        tail -n +2 > $outputFile

																											# End of remove_duplicate_sequence.shx
