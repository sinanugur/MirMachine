Output
======

The ``MirMachine`` main executable will generate GFF annotations (filtered and unfiltered) and some other files.
You will see ``results/predictions/`` directory which contains:

``filtered_gff/`` **High confidence miRNA family predictions after bitscore filtering. (This file is what you need in most cases)**

``gff/`` **All predicted miRNA families.** You can access all the predictions without filtering.

``fasta/`` **Both high and low confidence predictions in FASTA format.** Both predictions from filtered and unfiltered are included and you access FASTA sequences. See explanation of FASTA identifiers.

Explanation of GFF files
------------------------

**Header:**

.. code-block::

    ##gff-version 3
    # MirMachine version: (MirMachine version used)
    # CM Models: Built using MirGeneDB 2.1 (DB version, usually suggests new families were included)
    # Total families searched: (Total families searched for this run)
    # Node: (Node name given)
    # Model: (selected model)
    # Genome file: (genome file location)
    # Species: (species name given)
    # Params: (Command line paramaters)
    # miRNAs families searched: (searched families)
    # Expected miRNA family losses: (miRNA family losses for this Node)
    # miRNA score: (percent of miRNA families detected)

An example prediction:

.. code-block:: bash

    chrI	MirMachine	microRNA	9379947	9380005	57.4	-	.	gene_id=Mir-71.PRE;E-value=3e-10;sequence_with_30nt=TCACACACAGAGGTTGTCTGCTCTGAACGATGAAAGACATGGGTAGTGAGACGTCGGAGCCTCGTCGTATCACTATTCTGTTTTTCGCCGTCGGGATCGTGACCTGGAAGCTGTAAACT
    
    GFF prediction explanation:
    **chrI=**Chromosome name.
    **MirMachine=**Source of the prediction.
    **microRNA=**Type of the feature.
    **9379947=**Start position of the feature.
    **9380005=**End position of the feature.
    **57.4=**Bitscore of the prediction.
    **-=**Strand of the feature.
    **gene_id=**miRNA family name.
    **E-value=**E-value of the prediction.
    **sequence_with_30nt=**Sequence of the miRNA hit and its 30nts upstream/downstream sequences.

`Read about GFF3 file format <https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md>`_

FASTA files
-----------

Example FASTA of a prediction:

.. code-block:: bash

    >Mir-9.PRE_chrI_9332963_9333028_(+)_56.8_HIGHconf_p5_seed(CTTTGGT)_p3_seed(AAAGCTA,TAAAGCT)
    TCTTTGGTGATTCAGCTTCAATGATTGGCTACAGGTTTCTTTCATAAAGCTAGGTTACCAAAGCTC


    Header explanation:
    >miRNA family name_chromosome_location_strand_bitscore_confidence_seed_sequences_detected
    #This is a high confidence prediction and we found three seeds both in the 5' and 3' ends of the miRNA.