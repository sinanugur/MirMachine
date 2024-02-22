Options and Arguments
=====================

How to use MirMachine
---------------------

Required arguments for a MirMachine run are: ``--node``, ``--species`` and ``--genome``.

You can select any name for **species name**. It is simply defines how you want to name your run.

The **genome file** must be a FASTA file. Its location is not important.

**A standard run:**

.. code-block:: bash

    MirMachine.py --node Caenorhabditis --species foo --genome /path/tp/genome/example.fasta

This will start a MirMachine run and search for all miRNAs belong to **Caenorhabditis** node.

What is a node and How to see available nodes?
----------------------------------------------
A node is a taxanomic node name to query the correct group of miRNA families. 

For example, **Caenorhabditis** node contains all miRNA families that are expected to be found in **Caenorhabditis** species.

You can query all available nodes with:

.. code-block:: bash

    MirMachine.py --print-all-nodes

Selection of a correct node is important for accurate prediction with fewer false positives. This will also reduce run time.

Which families are available in a node?
---------------------------------------

You can see that with:

.. code-block:: bash

    MirMachine.py --node Caenorhabditis

This will show the miRNA families that will be searched by MirMachine if you select **Caenorhabditis** node. These miRNA families are expected to be found by MirMachine.

What is a model and how to select a model?
------------------------------------------

MirMachine has three models: **deutero**, **proto** and **combined**. 
Combined means the covariance models were built using all MirGeneDB species. 

Proto and deutero were built using only proto and deutero species, respectively. In theory, proto and deutero models should be more accurate.

**All options and arguments:**

.. code-block::

    Usage:
        MirMachine.py --node <text> --species <text> --genome <text> [--model <text>] [--cpu <integer>] [--add-all-nodes|--single-node-only] [--unlock|--remove] [--touch] [--dry]
        MirMachine.py --species <text> --genome <text> --family <text> [--model <text>] [--cpu <integer>] [--unlock|--remove] [--touch] [--dry]
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
        --touch                             Touch output files (mark them up to date without really changing them).
        --version                           Show version.

Troubleshooting
---------------

**Dry run:**
You can test a run with ``--dry``. It shows which files will be generated.

**Unlocking the directory:**
If a job ends prematurely, Snakemake may lock the directory. You may have to rerun with ``--unlock`` argument. This will unlock the directory.

**Cleaning the output files:**
You can clean the output files with ``--remove`` argument.

**Touching the output files:**
You can touch the output files with ``--touch`` argument. This will mark the output files as up to date without really changing them.
