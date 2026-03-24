Core Concepts
=============

MirMachine runs are controlled by four main ideas: ``node``, ``family``,
``model``, and ``score``.

Node
----

A ``node`` is a taxonomic label used to select expected miRNA families.

* Use ``--node <name>`` to choose the query node.
* Use ``--print-all-nodes`` to list valid node names.
* Use ``MirMachine.py --node <name>`` (without ``--species`` and ``--genome``)
  to print families linked to that node.

Family
------

A ``family`` is a single miRNA family name (for example ``Let-7``).

* Use ``--family <name>`` for one-family runs.
* Family mode does not require ``--node``.
* Use ``--print-all-families`` to list available families for each model.

Model
-----

MirMachine supports three covariance-model sets:

* ``combined`` (default): models built across all supported taxa
* ``proto``: proto-specific model set
* ``deutero``: deutero-specific model set

Model choice affects which family CMs are available and the cutoff file used
for confidence filtering.

Search Scope Controls
---------------------

By default, MirMachine searches ancestor nodes for the selected query.

* ``--single-node-only`` limits searched families to exactly the selected node.
* ``--add-all-nodes`` expands the search with descendant nodes.

These flags only apply to ``--node`` runs.

Scoring and Confidence
----------------------

Each hit receives a CM bitscore and E-value.

* ``--evalue`` controls ``cmsearch --incE`` (default: ``0.2``).
* Family-specific trusted cutoffs are then applied to classify filtered
  predictions.
* GFF headers include a miRNA score (percent of detected families among searched
  families).

Input Expectations
------------------

* ``--genome`` must point to an uncompressed FASTA file.
* ``--species`` is the run label used in output filenames and YAML config names.
