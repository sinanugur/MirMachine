CLI Options and Arguments
=========================

Command Modes
-------------

MirMachine supports these invocation modes:

.. code-block:: text

    MirMachine.py --node <text> --species <text> --genome <text> [options]
    MirMachine.py --species <text> --genome <text> --family <text> [options]
    MirMachine.py --node <text> [--add-all-nodes]
    MirMachine.py --print-all-nodes
    MirMachine.py --print-all-families
    MirMachine.py --print-ascii-tree
    MirMachine.py (-h | --help)
    MirMachine.py --version

Run Examples
------------

Node-based run:

.. code-block:: bash

    MirMachine.py --node Caenorhabditis --species ce11 \
                 --genome /path/to/genome.fa --model combined

Single-family run:

.. code-block:: bash

    MirMachine.py --species ce11_let7 --genome /path/to/genome.fa \
                 --family Let-7

Show families for a node:

.. code-block:: bash

    MirMachine.py --node Caenorhabditis

Arguments
---------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Short
     - Long
     - Description
   * - ``-n``
     - ``--node <text>``
     - Node name (example: ``Caenorhabditis``).
   * - ``-s``
     - ``--species <text>``
     - Species/run label used in output filenames and YAML config.
   * - ``-g``
     - ``--genome <text>``
     - Path to uncompressed genome FASTA.
   * - ``-m``
     - ``--model <text>``
     - Model set: ``combined``, ``proto``, or ``deutero`` (default: ``combined``).
   * - ``-f``
     - ``--family <text>``
     - Search only one miRNA family (example: ``Let-7``).
   * - ``-e``
     - ``--evalue <float>``
     - Inclusion threshold passed to ``cmsearch --incE`` (default: ``0.2``).
   * - ``-c``
     - ``--cpu <integer>``
     - Parallel jobs passed to Snakemake (default: ``2``).

Options
-------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Flag
     - Description
   * - ``-a``, ``--add-all-nodes``
     - Expand node query to include descendants (broader family set).
   * - ``-o``, ``--single-node-only``
     - Limit searched families to only the selected node.
   * - ``-p``, ``--print-all-nodes``
     - Print available node names and exit.
   * - ``-l``, ``--print-all-families``
     - Print families available in each model and exit.
   * - ``-t``, ``--print-ascii-tree``
     - Print an ASCII representation of the taxonomy tree and exit.
   * - ``-u``, ``--unlock``
     - Unlock a stalled Snakemake working directory.
   * - ``-r``, ``--remove``
     - Delete all generated output files tracked by the workflow.
   * - ``-d``, ``--dry``
     - Dry-run the Snakemake DAG without executing jobs.
   * - ``--touch``
     - Mark targets as up-to-date without re-running jobs.
   * - ``--long``
     - Use long-miRNA covariance models from ``mirmachine/meta/lcms``.
   * - ``-h``, ``--help``
     - Show help text and exit.
   * - ``--version``
     - Show MirMachine version and exit.

Notes
-----

* ``--family`` mode does not require ``--node``.
* If ``--node`` is invalid, MirMachine prints valid nodes and exits.
* Model name validation is strict: ``combined``, ``proto``, ``deutero``.
