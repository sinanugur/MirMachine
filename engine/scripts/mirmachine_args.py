import os
import subprocess
from pathlib import Path

base_dir = os.path.dirname(__file__)
mirmachine_path = os.path.join(base_dir, '../mirmachine/')
meta_directory = os.path.join(mirmachine_path, 'meta')
workflows_dir = os.path.join(mirmachine_path, 'workflows/')


def run_mirmachine(job_object):
    Path("engine/data/yamls").mkdir(parents=True, exist_ok=True)
    Path("engine/data/temp").mkdir(parents=True, exist_ok=True)

    gen_file_path = 'data/temp/' + job_object.species + '.txt'
    try:
        write_genome_to_temp_file(job_object, 'engine/' + gen_file_path)
    except OSError:
        if os.path.exists('engine/' + gen_file_path):
            os.remove('engine/' + gen_file_path)
            write_genome_to_temp_file(job_object, 'engine/' + gen_file_path)

    both_ways = ''  # "--add-all-nodes" if arguments["--add-all-nodes"] else ""
    dry_run = ''  # "-n" if arguments["--dry"] else ""
    unlock = ''  # "--unlock" if arguments["--unlock"] else ""
    remove = ''  # "--delete-all-output" if arguments["--remove"] else ""
    default_node_argument = "" if job_object.single_node else "| while read i; do mirmachine_tree_parser.py {meta_directory}/tree.newick $i {both_ways}; done".format(
        meta_directory=meta_directory, both_ways=both_ways)

    if job_object.single_fam_mode:
        yaml_argument = """echo {family} | awk -v genome={genome} -v species={species} -v node={node} 'BEGIN{{print "genome: "genome;print "species: "species;print "node: "node; print "mirnas:"}}{{print " - "$1}}' > engine/data/yamls/{species}.yaml""".format(
            family=job_object.family,
            species=job_object.species,
            node=job_object.node,
            genome=gen_file_path)

    else:
        yaml_argument = """echo {node} {default_node_argument} | sort | uniq | while read a; \
        do grep $a {meta_directory}/nodes_mirnas_corrected.tsv; done \
        | grep -v NOVEL | grep -v NA | cut -f2 | sort | uniq | \
        awk -v genome={genome} -v species={species} -v node={node} 'BEGIN{{print "genome: "genome;print "species: "species;print "node: "node; print "mirnas:"}}{{print " - "$1}}' > engine/data/yamls/{species}.yaml""".format(
            default_node_argument=default_node_argument,
            meta_directory=meta_directory,
            node=job_object.node,
            mirmachine_path=mirmachine_path,
            species=job_object.species,
            genome=gen_file_path)

    out = subprocess.run(yaml_argument, shell=True)

    if out.returncode != 0:
        return out, job_object

    snakemake_argument="snakemake -s engine/mirmachine/workflows/mirmachine_search.smk -d {workdir} " \
                       "--rerun-incomplete --config meta_directory={meta_directory} model={model} " \
                       "mirmachine_path={mirmachine_path} --configfile engine/data/yamls/{species}.yaml " \
                       "--cores {cpu}".format(
        species=job_object.species,
        cpu=4,
        workdir='engine/',
        model=job_object.model_type,
        meta_directory=meta_directory,
        mirmachine_path=mirmachine_path)

    out = subprocess.run(snakemake_argument, shell=True)
    return out, job_object


def write_genome_to_temp_file(job_object, gen_file_path):
    genome_file = open(gen_file_path, 'x')
    genome_file.write('>{species}\n'.format(species=job_object.species))
    genome_file.write(job_object.data)
    genome_file.close()
