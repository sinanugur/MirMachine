Installation
============

Recommended: Conda/Mamba (Bioconda)
-----------------------------------

Install from Bioconda with conda:

.. code-block:: console

    conda install mirmachine -c bioconda -c conda-forge

Using mamba is faster for dependency solving:

.. code-block:: console

    conda install mamba -c conda-forge
    mamba install mirmachine -c bioconda -c conda-forge


From Source (Local Development)
-------------------------------

From the repository root:

.. code-block:: console

    conda env create -f environment.yml
    conda activate mirmachine
    pip install -e .

MirMachine now ships a ``pyproject.toml`` build definition, so pip installs use
the standard PEP 517 build backend by default.

The environment file includes Python dependencies plus required command-line
tools used by the workflow (for example ``snakemake``, ``infernal``,
``samtools``, ``bedtools``, ``gawk``, and ``moreutils``).

Verify Installation
-------------------

Check CLI availability:

.. code-block:: console

    MirMachine.py --help
