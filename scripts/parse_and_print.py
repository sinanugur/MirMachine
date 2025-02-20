#!/usr/bin/env python3

import sys

def parse_lines(lines):
    parsed_data = {}

    for line in lines:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue

        # Only process lines starting with # (one or more)
        if line.startswith("#"):
            # Strip all leading '#' characters
            stripped = line.lstrip('#').strip()
            
            # Case 1: If there's a colon, split by the first colon
            if ':' in stripped:
                parts = stripped.split(':', 1)
                key = parts[0].strip()
                value = parts[1].strip()
                parsed_data[key] = value
            else:
                # Case 2: No colon. e.g. "gff-version 3"
                # Split by whitespace into key/value
                parts = stripped.split(None, 1)
                if len(parts) == 2:
                    key, value = parts
                    parsed_data[key] = value
                else:
                    # If there's only one part, decide how to handle it.
                    # Here, we'll just ignore it.
                    pass

    return parsed_data

if __name__ == "__main__":
    # Read all lines from standard input
    lines = sys.stdin.readlines()

    # Parse the lines
    parsed_data = parse_lines(lines)

    # Print results to STDOUT
    for key, value in parsed_data.items():
        print(f"{key}: {value}")

