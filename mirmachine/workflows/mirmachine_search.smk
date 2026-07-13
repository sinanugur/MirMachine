# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''
Created on 03/08/2020

MirMachine snakemake workflow

@author: Sinan U. Umu, sinanugur@gmail.com
'''
__version__="0.3.0.5"
MDBver="3.0"

__licence__="""
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


from collections import defaultdict
import os.path
from yaml import load

genome=config['genome']
params=config['params']
species=config['species']
node=config['node']
model=config.get('model','combined')
nonull3="" if config.get('nonull3','No') == 'No' else "--nonull3"
inclusion_threshold=config.get('evalue',0.2) #default inclusion threshold, I think this is not same for cmsearch by default
meta_directory=config.get('meta_directory','meta')
cm_directory=config.get('cm_directory', meta_directory + "/cms")
mirmachine_path=config.get('mirmachine_path','mirmachine')
mirna=[x.title() + ".PRE" for x in config['mirnas']]
score_mirna=[x.title() + ".PRE" for x in config.get('score_mirnas', config['mirnas'])]

if config.get('losses',[]):
	losses=[x.title() + ".PRE" for x in config.get('losses',[])]
else:
	losses=[]


cutoff_file=meta_directory + "/cutoffs/" + model + "/mirmachine_trusted_cutoffs.tsv"

nodes_mirnas_file=meta_directory + "/nodes_mirnas_corrected.tsv"
#losses_mirnas_file=meta_directory + "/losses_mirnas.tsv"
seeds_file=meta_directory + "/family_seeds.tsv"


#pull out CMs, I added this part to check ready models
#files, = glob_wildcards("analyses/cms/{files}.CM")

#mirna_from=config.get('read_mirnas_from_cm_folder','No')

#if mirna_from == "Yes":
#	mirna=files


available_mirnas=glob_wildcards(cm_directory + "/" + model + "/{mirna}.CM").mirna

missing_mirnas=[item for item in mirna if item not in available_mirnas]
#print("Available mirnas: ",available_mirnas)
if missing_mirnas:
	print("Warning missing microRNAs: ",missing_mirnas)
	print("Consider changing the model to combined if you are searching for proto or deutero microRNAs.")
	print("If you selected -a option, nothing to worry about.")
#print("Losses: ",losses)


mirnas_to_search=[item for item in mirna if item not in losses and item not in missing_mirnas] #remove losses and missing mirnas from the list
score_missing_mirnas=[item for item in score_mirna if item not in available_mirnas]
mirnas_for_score=[item for item in score_mirna if item not in losses and item not in score_missing_mirnas]
mirnas_to_search_upper=[item.upper() for item in mirnas_to_search]
losses_upper=[item.upper() for item in losses]
mirnas_for_score_upper=[item.upper() for item in mirnas_for_score]
mirnas_for_score_csv=",".join(mirnas_for_score_upper)

cutoffs_dict=defaultdict(int)
with open(cutoff_file) as tsv:
	for line in tsv.readlines():
		cutoffs_dict[line.split()[0] + ".PRE"]=line.split()[1]

nodes_mirnas_dict=defaultdict(str)
with open(nodes_mirnas_file) as tsv:
	for line in tsv.readlines():
		nodes_mirnas_dict[line.split()[1].title() + ".PRE"]=line.split()[0]


seeds_dict=defaultdict(dict)
with open(seeds_file) as tsv:
	for line in tsv.readlines():
		#Bantam_3p       NA      AAAGACC
		#1	Bantam_3p	NA	AAAGACC	Bantam	81	Low conf
		#m=line.split()[1].split("_")[0].strip().title() + ".PRE"
		fam=line.split("\t")[4].strip().title() + ".PRE"
		if "5p" not in seeds_dict[fam]:
			seeds_dict[fam]["5p"]=list()
		if "3p" not in seeds_dict[fam]:
			seeds_dict[fam]["3p"]=list()
		if line.split("\t")[2].strip() != "NA":
			s5=line.split("\t")[2].strip()
			seeds_dict[fam]["5p"].append(s5 + "*" if line.split("\t")[6][0].strip() == "H" else s5)
		if line.split("\t")[3].strip() != "NA":
			s3=line.split("\t")[3].strip()
			seeds_dict[fam]["3p"].append(s3 + "*" if line.split("\t")[6][0].strip() == "H" else s3)

gffheader="""##gff-version 3
# MirMachine version: {version}
# CM Models: Built using MirGeneDB {MDBver}
# Total families searched: {total}
# Node: {node}
# Model: {model}
# Genome file: {genome}
# Species: {species}
# Params: {params}
# microRNA families searched: {mirna}
# Expected microRNA family losses: {losses} 
# microRNA score: __MM_HIT_SCORE__
# microRNA seed score: __MM_SEED_SCORE__
# microRNA hiconf seed score: __MM_HICONF_SEED_SCORE__ """.format(version=__version__,MDBver=MDBver,total=len(mirnas_to_search),score_total=len(mirnas_for_score),node=node,model=model,genome=genome,species=species,mirna=mirnas_to_search_upper,params=params,losses=losses_upper)

#print (gffheader)

rule all:
	input:
		expand("results/predictions/gff/{species}.PRE.gff",species=species),
		expand("results/predictions/filtered_gff/{species}.PRE.gff",species=species),
		expand("results/predictions/heatmap/{species}.heatmap.csv",species=species),
		expand("results/predictions/fasta/{species}.PRE.fasta",species=species)


rule prepare_genome:
	input:
		genome
	output:
		temp("data/genomes/" + species + ".fai"),
		temp("data/genomes/" + species + ".size")
		#genome + ".fai",
		#genome + ".size"
	shell:
		"""
		samtools faidx {input};
		mv {genome}.fai {output[0]};
		cut -f1,2 {output[0]} > {output[1]};
		"""
rule search_CM:
	input:
		cm_directory + "/" + model + "/{mirna}.CM"
	output:
		"analyses/output/{species}/{mirna}.result"
	threads: 4
	shell:
		"""
		cmsearch {nonull3} --incE {inclusion_threshold} --cpu {threads} {input} {genome} > {output}

		"""
rule parse_output:
	input:
		"analyses/output/{species}/{mirna}.result",
		"data/genomes/" + species + ".size"
		#genome + ".size"
	output:
		"analyses/output/{species}/{mirna}.gff",
		temp("analyses/output/{species}/{mirna}.ext.gff"),
		"analyses/output/{species}/{mirna}.unfiltered"

	params:
		parse=r""" 'match($0,/\([0-9]+\)\s+!\s+.*/,m){{if($9 =="+") {{start=$7;end=$8}} else {{start=$8;end=$7}}; print $6"\tMirMachine\tmicroRNA\t"start"\t"end"\t"$4"\t"$9"\t.\tgene_id="toupper(id)";E-value="$3}}' """,

	shell:
		"""
		#parse the result file into GFF file
		awk '{{print}} /Hit alignments/ {{exit}}' {input[0]} | gawk -v id={wildcards.mirna} {params.parse} | gawk '($5-$4)>=50{{print}}' > {output[0]}
		bedtools slop -i {output[0]} -g {input[1]} -b 30 > {output[1]}

		#write the sequences into the GFF file
		paste --delimiters=";" {output[0]} <(bedtools getfasta -tab -s -fi {genome} -bed {output[1]} | awk '{{print "sequence_with_30nt="$2}}') > {output[2]}

		#sort and filter overlapping
		gff_sort_and_compete.sh {output[2]} > {output[0]}
		"""

rule create_filtered_gffs:
	input:
		"analyses/output/{species}/{mirna}.gff",
		cutoff_file
	output:
		temp("analyses/output/{species}/{mirna}.filtered.gff")

	params:
		trusted=lambda wildcards: cutoffs_dict[wildcards.mirna]
	
	run:
		shell("cat {input[0]} | awk -v trusted={params.trusted} '$6 >= trusted{{print}}' > {output}")

rule fastas:
	input:
		"analyses/output/{species}/{mirna}.gff",
		cutoff_file
	output:
		#temp("analyses/output/{species}/{mirna}.filtered.fasta")
		"analyses/output/{species}/{mirna}.filtered.fasta"
	params:
		trusted=lambda wildcards: cutoffs_dict[wildcards.mirna],
		seeds5=lambda wildcards: seeds_dict[wildcards.mirna]["5p"],
		seeds3=lambda wildcards: seeds_dict[wildcards.mirna]["3p"]
	shell:
		"""
		paste <(cat {input[0]} | gawk -v id={wildcards.mirna} -v trusted={params.trusted} '{{if($6 >= trusted) o="HIGHconf"; else o="LOWconf"; print ">"toupper(id)"_"$1"_"$4"_"$5"_("$7")_"$6"_"o}}') <(bedtools getfasta -tab -s -fi {genome} -bed {input[0]} | awk '{{print $2}}') | awk '{{print $1"\\n"$2}}' > {output}
		seed_detector.py {output} '{params.seeds5}' '{params.seeds3}' | sponge {output}
		"""
		
rule combine_fastas:
	input:
		expand(r"analyses/output/{species}/{mirna}.filtered.fasta",species=species,mirna=mirnas_to_search)
	output:
		"results/predictions/fasta/{species}.PRE.fasta"
	run:
		shell("cat {input} | awk '{{print}}' > {output}")




rule combine_gffs:
	input:
		gff_files=expand("analyses/output/{species}/{mirna}.gff",species=species,mirna=mirnas_to_search),
		fasta_file="results/predictions/fasta/{species}.PRE.fasta"
	output:
		"results/predictions/gff/{species}.PRE.gff"
	params:
		header=gffheader,
		total=len(mirnas_for_score),
		score_mirna=mirnas_for_score_csv
	run:
		shell("""echo "{params.header}" > {output}""")
		#shell("cat analyses/output/{wildcards.species}/*PRE.gff | awk '/PRE/' >> {output}")
		shell("cat {input.gff_files} | awk '/PRE/' >> {output}")
		shell("cat {output} | seed_merger.sh {input.fasta_file} | sponge {output}")
		shell("""
		SCORES=$(gawk -v total={params.total} -v scored="{params.score_mirna}" '
		BEGIN{{split(scored, s, ","); for (i in s) {{allowed[s[i]]=1;}}}}
		match($0,"gene_id=([^;]+)[.]PRE",m) {{
			fam=toupper(m[1])".PRE";
			if (fam in allowed) {{
				hit[fam]=1;
				if ($0 !~ /seed=\\(None\\)/) {{
					seed[fam]=1;
					if (index($0,"*") > 0) hiseed[fam]=1;
				}}
			}}
		}}
		END {{
			if(total==0) print "0 0 0";
			else printf "%.4f %.4f %.4f\\n", (length(hit)/total)*100, (length(seed)/total)*100, (length(hiseed)/total)*100;
		}}' {output})
		set -- $SCORES
		SCORE=${{1:-0}}
		SEED_SCORE=${{2:-0}}
		HICONF_SEED_SCORE=${{3:-0}}
		gawk -v score="$SCORE" -v seed_score="$SEED_SCORE" -v hiconf_seed_score="$HICONF_SEED_SCORE" '{{gsub("__MM_HIT_SCORE__", score); gsub("__MM_SEED_SCORE__", seed_score); gsub("__MM_HICONF_SEED_SCORE__", hiconf_seed_score); print}}' {output} | sponge {output}
		""")

rule combine_filtered_gffs:
	input:
		gff_files=expand("analyses/output/{species}/{mirna}.filtered.gff",species=species,mirna=mirnas_to_search),
		fasta_file="results/predictions/fasta/{species}.PRE.fasta"
	output:
		"results/predictions/filtered_gff/{species}.PRE.gff"
	params:
		header=gffheader,
		total=len(mirnas_for_score),
		score_mirna=mirnas_for_score_csv
	run:
		shell("""echo "{params.header}" > {output}""")
		#shell("cat analyses/output/{wildcards.species}/*PRE.filtered.gff | awk '/PRE/' >> {output}")
		shell("cat {input.gff_files} | awk '/PRE/' >> {output}")
		shell("cat {output} | seed_merger.sh {input.fasta_file} | sponge {output}")
		shell("""
		SCORES=$(gawk -v total={params.total} -v scored="{params.score_mirna}" '
		BEGIN{{split(scored, s, ","); for (i in s) {{allowed[s[i]]=1;}}}}
		match($0,"gene_id=([^;]+)[.]PRE",m) {{
			fam=toupper(m[1])".PRE";
			if (fam in allowed) {{
				hit[fam]=1;
				if ($0 !~ /seed=\\(None\\)/) {{
					seed[fam]=1;
					if (index($0,"*") > 0) hiseed[fam]=1;
				}}
			}}
		}}
		END {{
			if(total==0) print "0 0 0";
			else printf "%.4f %.4f %.4f\\n", (length(hit)/total)*100, (length(seed)/total)*100, (length(hiseed)/total)*100;
		}}' {output})
		set -- $SCORES
		SCORE=${{1:-0}}
		SEED_SCORE=${{2:-0}}
		HICONF_SEED_SCORE=${{3:-0}}
		gawk -v score="$SCORE" -v seed_score="$SEED_SCORE" -v hiconf_seed_score="$HICONF_SEED_SCORE" '{{gsub("__MM_HIT_SCORE__", score); gsub("__MM_SEED_SCORE__", seed_score); gsub("__MM_HICONF_SEED_SCORE__", hiconf_seed_score); print}}' {output} | sponge {output}
		""")


rule mirna_node_tmp_file:
	input:
		nodes_mirnas_file
	output:
		"analyses/search/{species}.mirna_nodes.csv"
	run:
		for i in mirna:
			node=nodes_mirnas_dict[i]
			o=i.replace(".PRE", "").upper()
			shell("""echo {o}","{node} >> {output}""")



rule create_heatmap_csv:
	input:
		"results/predictions/gff/{species}.PRE.gff",
		"results/predictions/filtered_gff/{species}.PRE.gff",
		"analyses/search/{species}.mirna_nodes.csv"

	output:
		temp("results/predictions/gff/{species}.csv"),
		temp("results/predictions/filtered_gff/{species}.csv"),
		temp("results/predictions/heatmap/{species}.csv"),
		"results/predictions/heatmap/{species}.heatmap.csv"

	params:
		header=gffheader
	run:
		shell("""
			gawk 'match($0,"gene_id=([^;]+)[.]PRE",m) {{print m[1]}}' {input[0]} | sort | uniq -c | awk '{{print $2","$1}}' | sort -t, -k1,1 > {output[0]}
			gawk 'match($0,"gene_id=([^;]+)[.]PRE",m) {{print m[1]}}' {input[1]} | sort | uniq -c | awk '{{print $2","$1}}' | sort -t, -k1,1 > {output[1]}
			gawk 'match($0,"gene_id=([^;]+)[.]PRE",m) {{if ($0 !~ /seed=\\(None\\)/) print m[1]}}' {input[0]} | sort | uniq -c | awk '{{print $2","$1}}' | sort -t, -k1,1 > {output[2]}.unfiltered_seed.tmp
			gawk 'match($0,"gene_id=([^;]+)[.]PRE",m) {{if ($0 !~ /seed=\\(None\\)/) print m[1]}}' {input[1]} | sort | uniq -c | awk '{{print $2","$1}}' | sort -t, -k1,1 > {output[2]}.filtered_seed.tmp
			gawk 'match($0,"gene_id=([^;]+)[.]PRE",m) {{if ($0 !~ /seed=\\(None\\)/ && index($0,"*") > 0) print m[1]}}' {input[0]} | sort | uniq -c | awk '{{print $2","$1}}' | sort -t, -k1,1 > {output[2]}.unfiltered_hiconf_seed.tmp
			gawk 'match($0,"gene_id=([^;]+)[.]PRE",m) {{if ($0 !~ /seed=\\(None\\)/ && index($0,"*") > 0) print m[1]}}' {input[1]} | sort | uniq -c | awk '{{print $2","$1}}' | sort -t, -k1,1 > {output[2]}.filtered_hiconf_seed.tmp

				gawk -F, 'BEGIN{{OFS=","}} FNR==NR{{u[$1]=$2; next}} ARGIND==2{{f[$1]=$2; next}} ARGIND==3{{us[$1]=$2; next}} ARGIND==4{{fs[$1]=$2; next}} ARGIND==5{{uhs[$1]=$2; next}} ARGIND==6{{fhs[$1]=$2; next}} {{print $1,$2,($1 in u ? u[$1] : 0),($1 in f ? f[$1] : 0),($1 in us ? us[$1] : 0),($1 in fs ? fs[$1] : 0),($1 in uhs ? uhs[$1] : 0),($1 in fhs ? fhs[$1] : 0)}}' {output[0]} {output[1]} {output[2]}.unfiltered_seed.tmp {output[2]}.filtered_seed.tmp {output[2]}.unfiltered_hiconf_seed.tmp {output[2]}.filtered_hiconf_seed.tmp {input[2]} > {output[2]}
				rm -f {output[2]}.unfiltered_seed.tmp {output[2]}.filtered_seed.tmp {output[2]}.unfiltered_hiconf_seed.tmp {output[2]}.filtered_hiconf_seed.tmp

		echo "{params.header}" | grep -v "__MM_" > {output[3]}
		grep -E "^# microRNA .*score" {input[0]} | sed 's/^# microRNA /# microRNA unfiltered /' >> {output[3]}
		grep -E "^# microRNA .*score" {input[1]} >> {output[3]}
			awk -F, -v species={wildcards.species} -v query_node={node} 'BEGIN{{OFS=","; print "species,query_node,family,node,total_hits,filtered_hits,unfiltered_seed,filtered_seed,unfiltered_hiconf_seed,filtered_hiconf_seed"}}{{print species,query_node,$1,$2,$3,$4,$5,$6,$7,$8}}' {output[2]} >> {output[3]}


		""")
