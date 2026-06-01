Output
======

MirMachine writes intermediate files under ``data/`` and ``analyses/`` and
final run outputs under ``results/predictions/``.

Main Output Layout
------------------

For ``--species ExampleSpecies``, the key files are:

.. code-block:: text

    data/yamls/ExampleSpecies.yaml
    results/predictions/gff/ExampleSpecies.PRE.gff
    results/predictions/filtered_gff/ExampleSpecies.PRE.gff
    results/predictions/fasta/ExampleSpecies.PRE.fasta
    results/predictions/heatmap/ExampleSpecies.heatmap.csv

Interpretation
--------------

``results/predictions/gff/*.PRE.gff``
  Unfiltered predictions after overlap resolution.

``results/predictions/filtered_gff/*.PRE.gff``
  High-confidence subset after family-specific trusted cutoff filtering.

``results/predictions/fasta/*.PRE.fasta``
  FASTA entries for predicted loci, including confidence label and seed
  annotations in the header.

``results/predictions/heatmap/*.heatmap.csv``
  Summary table for downstream plotting with per-family total and filtered hit
  counts.

GFF Header Fields
-----------------

**Header:**

.. code-block::

    ##gff-version 3
    # MirMachine version: (MirMachine version used)
    # CM Models: Built using MirGeneDB 3.0 (database version)
    # Total families searched: (Total families searched for this run)
    # Node: (Node name given)
    # Model: (selected model)
    # Genome file: (genome file location)
    # Species: (species name given)
    # Params: (Command line parameters)
    # microRNA families searched: (searched families)
    # Expected microRNA family losses: (microRNA family losses for this Node)
    # microRNA score: (percent of score families with >=1 hit)
    # microRNA seed score: (percent of score families with >=1 hit that has seed != None)
    # microRNA hiconf seed score: (percent of score families with >=1 hit that has at least one * seed)

The filtered and unfiltered files each contain all three scores in the header.

Example GFF Row
---------------

An example prediction line:

.. code-block:: bash

    chrI	MirMachine	microRNA	9379947	9380005	57.4	-	.	gene_id=Mir-71.PRE;E-value=3e-10;sequence_with_30nt=TCACACACAGAGGTTGTCTGCTCTGAACGATGAAAGACATGGGTAGTGAGACGTCGGAGCCTCGTCGTATCACTATTCTGTTTTTCGCCGTCGGGATCGTGACCTGGAAGCTGTAAACT

Field meanings:

* ``chrI``: chromosome/contig name
* ``MirMachine``: annotation source
* ``microRNA``: feature type
* ``9379947`` and ``9380005``: start/end
* ``57.4``: CM bitscore
* ``-``: strand
* ``gene_id``: miRNA family ID
* ``E-value``: hit E-value
* ``sequence_with_30nt``: hit sequence with 30 nt flanks

`Read about GFF3 file format <https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md>`_

FASTA files
-----------

Example FASTA of a prediction:

.. code-block:: bash

    >Mir-9.PRE_chrI_9332963_9333028_(+)_56.8_HIGHconf_p5_seed(CTTTGGT)_p3_seed(AAAGCTA,TAAAGCT)
    TCTTTGGTGATTCAGCTTCAATGATTGGCTACAGGTTTCTTTCATAAAGCTAGGTTACCAAAGCTC

Header pattern:

.. code-block:: text

    >family_chr_start_end_(strand)_bitscore_confidence_seed_annotations

Confidence values are ``HIGHconf`` or ``LOWconf``.

Heatmap CSV
-----------

``results/predictions/heatmap/<species>.heatmap.csv`` includes metadata lines
from the GFF header followed by a CSV table with this schema:

.. code-block:: text

    species,query_node,family,node,total_hits,filtered_hits,unfiltered_seed,filtered_seed,unfiltered_hiconf_seed,filtered_hiconf_seed
