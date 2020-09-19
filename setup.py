from setuptools import setup, find_packages

with open("requirements.txt") as req:
    requirements=req.readlines()

setup(
    name="miRmachine",
    version="0.1.0",
    packages=find_packages(),
    #scripts=["bin/*.py"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=requirements,

    include_package_data=True,

    # metadata to display on PyPI
    author="Sinan U. Umu",
    author_email="sinanugur@gmail.com",
    description="miRmachine",
    keywords="RNA miRNA detection prediction",
    url="",   # project home page, if any
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

    # could also include long_description, download_url, etc.
)
