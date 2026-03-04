Quick Start
===========

Run MirMachine in a clean working directory. It writes intermediate files under
``data/`` and ``analyses/`` and final outputs under ``results/predictions/``.

Example 1: Standard Node-Based Run
----------------------------------

.. code-block:: bash

    MirMachine.py -n Caenorhabditis -s Caenorhabditis_elegans \\
                 --genome sample/genomes/ce11.fa \\
                 --model proto --cpu 20

This searches families associated with the ``Caenorhabditis`` node using the
``proto`` model set.

Example 2: Restrict to a Single Node Only
-----------------------------------------

.. code-block:: bash

    MirMachine.py --node Caenorhabditis --species ce11_single_node \\
                 --genome sample/genomes/ce11.fa --single-node-only

Use this when you do not want ancestor/descendant node expansion.

Example 3: Single-Family Run
----------------------------

.. code-block:: bash

    MirMachine.py --species ce11_let7 --genome sample/genomes/ce11.fa \\
                 --family Let-7 --model combined

This bypasses node selection and searches only the given miRNA family.

Discover Available Inputs
-------------------------

List valid nodes:

.. code-block:: bash

    MirMachine.py --print-all-nodes

List available families by model:

.. code-block:: bash

    MirMachine.py --print-all-families

Show families linked to a specific node:

.. code-block:: bash

    MirMachine.py --node Caenorhabditis

What Gets Created
-----------------

For species name ``Caenorhabditis_elegans``, MirMachine creates:

* ``data/yamls/Caenorhabditis_elegans.yaml`` (run config)
* ``results/predictions/gff/Caenorhabditis_elegans.PRE.gff``
* ``results/predictions/filtered_gff/Caenorhabditis_elegans.PRE.gff``
* ``results/predictions/fasta/Caenorhabditis_elegans.PRE.fasta``
* ``results/predictions/heatmap/Caenorhabditis_elegans.heatmap.csv``
