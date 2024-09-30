Quick start example
===================
Create a new directory and run MirMachine there after the installation. MirMachine will create the required directories while running.

Here's an example command for running MirMachine with specific parameters:

.. code-block:: bash

    MirMachine.py -n Caenorhabditis -s Caenorhabditis_elegans \\
                 --genome sample/genomes/ce11.fa -m proto --cpu 20

**Explanation of arguments:**

* `-n`: Species name (in this case, Caenorhabditis).
* `-s`: Species scientific name (Caenorhabditis_elegans).
* `--genome`: Path to the genome FASTA file (sample/genomes/ce11.fa).
* `-m`: Model type (proto in this case).
* `--cpu`: Number of CPUs to use (20).
