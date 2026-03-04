MirMachine Documentation
========================

MirMachine is a command line workflow for detecting conserved miRNA families
from genome FASTA files.

The ``MirMachine.py`` entry point prepares run metadata and launches a
Snakemake workflow that generates:

* unfiltered GFF predictions
* filtered (high-confidence) GFF predictions
* FASTA sequences for predicted loci
* heatmap-ready summary tables

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation.rst
   quick_start.rst
   concepts.rst
   output.rst
   options.rst
   trouble.rst
