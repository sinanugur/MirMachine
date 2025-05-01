# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from collections import defaultdict
import os.path
from yaml import load

genome = config['genome']
species = config['species']
meta_directory = config.get('meta_directory', 'meta')
model = "rfam"

output_directory = "analyses/rfam/output/"

__licence__ = """
MIT License

Copyright (c) 2020 Sinan Ugur Umu (SUU) sinanugur@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

# pull out CMs, I added this part to check ready models
files, = glob_wildcards("mirmachine/cms/meta/rfam/{mirna}.cm")

print(files)


rule all:
    input:
        # expand("analyses/rfam/output/{species}/{mirna}.result",species=species,mirna=files),
        # expand("analyses/rfam/output/{species}/{mirna}.gff",species=species,mirna=files)
        expand("results/predictions/rfam/{species}.rfam.gff", species=species)


rule prepare_genome:
    input:
        genome
    output:
        "data/genomes/" + species + ".fai",
        "data/genomes/" + species + ".size"

    shell:
        """
        samtools faidx {input};
        mv {genome}.fai {output[0]};
        cut -f1,2 {output[0]} > {output[1]};
        """

rule search_CM:
    input:
        "mirmachine/cms/meta/rfam/{mirna}.cm"

    output:
        "analyses/rfam/output/{species}/{mirna}.result"

    threads: 15
    shell:
        """
        cmsearch --rfam --cut_tc --cpu {threads} {input} {genome} > {output}

        """


rule parse_rfam_output:
    input:
        "analyses/rfam/output/{species}/{mirna}.result",
        "data/genomes/" + species + ".size"
        # genome + ".size"
    output:
        "analyses/rfam/output/{species}/{mirna}.gff",
        temp("analyses/rfam/output/{species}/{mirna}.ext.gff"),
        "analyses/rfam/output/{species}/{mirna}.unfiltered"

    params:
        parse = """ 'match($0,/\([0-9]+\)\s+!\s+.*/,m){{if($9 =="+") {{start=$7;end=$8}} else {{start=$8;end=$7}}; print $6"\tcmsearch\tncRNA\t"start"\t"end"\t"$4"\t"$9"\t.\tgene_id="id";rfam_id="rfam";E-value="$3}}' """,

    shell:
        """
        #parse the result file into GFF file
        gene_id=$(cat {input[0]} | gawk 'match($0,/Query:\s+(.*)\s/,m){{print m[1]}}')

        awk '{{print}} /Hit alignments/ {{exit}}' {input[0]} | gawk -v id=$gene_id -v rfam={wildcards.mirna} {params.parse} > {output[0]}
        bedtools slop -i {output[0]} -g {input[1]} -b 30 > {output[1]}

        #write the sequences into the GFF file
        paste --delimiters=";" {output[0]} <(bedtools getfasta -tab -s -fi {genome} -bed {output[1]} | awk '{{print "sequence_with_30nt="$2}}') > {output[2]}

        #sort and filter overlapping
        gff_sort_and_compete.sh {output[2]} > {output[0]}
        """


rule combine_filtered_gffs:
    input:
        expand(
            "analyses/rfam/output/{species}/{mirna}.gff", species=species, mirna=files)
    output:
        "results/predictions/rfam/{species}.rfam.gff"
    run:
        shell("cat analyses/rfam/output/{wildcards.species}/*.gff > {output}")
