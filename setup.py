from setuptools import setup, find_packages, Command
import os

with open("requirements.txt") as req:
    requirements=req.readlines()

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


with open("README.md","r") as readme:
    long_description=readme.read()

setup(
    name="MirMachine",
    version="0.3.0.1",
    packages=find_packages(exclude=('tests*','testing*')),
    scripts=["scripts/MirMachine.py","scripts/mirmachine-tree-parser.py","scripts/gff_sort_and_compete.sh","scripts/seed_detector.py","scripts/parse_and_print.py","scripts/seed_merger.sh"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={"dev":["pytest>=3.7"]},
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
    #data_files={"meta":["*.tsv"]},
    #package_data={'meta': ["*.tsv",'meta/*.tsv'], "workflows" : ["*.smk","workflows/*.smk"]},
    #data_files=[("mirmachine",["meta/cms/proto/*.CM"])],
    # metadata to display on PyPI
    author="Sinan U. Umu",
    author_email="sinanugur@gmail.com",
    description="MirMachine",
    keywords="RNA miRNA detection prediction",
        cmdclass={
        'clean': CleanCommand,
    },
    url="https://github.com/sinanugur/MirMachine",   # project home page, if any
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Topic :: Scientific/Engineering :: Bio-Informatics'

    ]

    # could also include long_description, download_url, etc.
)
