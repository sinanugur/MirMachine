#!/bin/bash
# usage: cat input.txt | ./script.sh seedfile.txt

# Ensure a seed file is provided.
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 seedfile" >&2
  exit 1
fi

seedfile="$1"

# Process each line from standard input.
while IFS= read -r line; do
  # If the line starts with "#", print as-is.
  if [[ $line =~ ^# ]]; then
    echo "$line"
  else
    # Split the line into whitespace-separated fields.
    # We extract the first, fourth, and fifth fields.
    read -r f1 f2 f3 f4 f5 _ <<< "$line"
    gene="${f1}_${f4}_${f5}"

    # Search the seed file for the gene.
    # Then use grep with Perl regex to extract anything between _seed( and )
    seed=$(grep "$gene" "$seedfile" | grep -oP '_seed\(\K.*?(?=\))')
    
    # Append the seed information to the original line.
    if [ -n "$seed" ]; then
      echo "${line};seed=(${seed})"
    else
      echo "${line};seed=(None)"
    fi
  fi
done

