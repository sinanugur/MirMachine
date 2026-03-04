Troubleshooting
===============

Common Issues and Fixes
-----------------------

Invalid node name
-----------------

Symptom:
  MirMachine prints an error panel saying the node is wrong.

Fix:

.. code-block:: bash

    MirMachine.py --print-all-nodes

Then choose one of the listed nodes.

Genome file error
-----------------

Symptom:
  MirMachine reports that the genome file does not exist.

Fix:

* Verify the path passed to ``--genome``.
* Use an uncompressed FASTA file.

Stalled Snakemake lock
----------------------

Symptom:
  Workflow stops because the working directory is locked.

Fix:

.. code-block:: bash

    MirMachine.py --node Caenorhabditis --species run1 --genome genome.fa --unlock

Workflow cleanup
----------------

Delete generated outputs:

.. code-block:: bash

    MirMachine.py --node Caenorhabditis --species run1 --genome genome.fa --remove

Mark targets as up to date:

.. code-block:: bash

    MirMachine.py --node Caenorhabditis --species run1 --genome genome.fa --touch

Dry-run before execution:

.. code-block:: bash

    MirMachine.py --node Caenorhabditis --species run1 --genome genome.fa --dry

Low-confidence or sparse predictions
------------------------------------

* Verify that node and model are biologically appropriate.
* Try ``--model combined`` if families are missing in ``proto`` or ``deutero``.
* Increase ``--evalue`` carefully to broaden inclusion (may increase low-quality
  hits).

Family not found in single-family mode
--------------------------------------

Use:

.. code-block:: bash

    MirMachine.py --print-all-families

Then pick a family name shown in the output.
