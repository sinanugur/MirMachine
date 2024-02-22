Troubleshooting
===============

**Dry run:**
You can test a run with ``--dry``. It shows which files will be generated.

**Unlocking the directory:**
If a job ends prematurely, Snakemake may lock the directory. You may have to rerun with ``--unlock`` argument. This will unlock the directory.

**Cleaning the output files:**
You can clean the output files with ``--remove`` argument.

**Touching the output files:**
You can touch the output files with ``--touch`` argument. This will mark the output files as up to date without really changing them.
