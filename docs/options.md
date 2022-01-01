# Options and Arguments

Required arguments for a MirMachine run are: __--node__, __--species__ and __--genome__.

You can select any name for **species name**. It is simply defines how you want to name your run.  

The **genome file** must be a FASTA file. Its location is not important.

For example:

`MirMachine.py --node Caenorhabditis --species foo --genome /path/tp/genome/example.fasta`

This will start a MirMachine run and search for all miRNAs belong to __Caenorhabditis__ node.

You can query all available nodes with: 

`MirMachine.py --print-all-nodes`

    


```
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
```

## Some examples



