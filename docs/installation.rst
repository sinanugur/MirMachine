Installation
============

**Using conda:**

To install this package with conda, run:

.. code-block:: console

    conda install mirmachine -c bioconda -c conda-forge

You may want to install Mamba first, which will reduce installation time. To install Mamba with conda, run:

.. code-block:: console

    conda install mamba -c conda-forge

Then, you can install MirMachine with Mamba:

.. code-block:: console

    mamba install mirmachine -c bioconda -c conda-forge

**Using pip:**

Alternatively, you can install MirMachine directly from GitHub using pip:

.. code-block:: console

    git clone https://github.com/sinanugur/MirMachine.git
    cd MirMachine
    pip install .

**Verifying installation:**

Once installed, you can verify if MirMachine is working by running the main script with the help flag:

.. code-block:: console

    MirMachine.py --help
