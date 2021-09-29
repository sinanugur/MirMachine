import os
import subprocess
import threading
from pathlib import Path

base_dir = os.path.dirname(__file__)
mirmachine_path = os.path.join(base_dir, '../mirmachine/')
meta_directory = os.path.join(mirmachine_path, 'meta')
workflows_dir = os.path.join(mirmachine_path, 'workflows/')
from snakemake import snakemake


def run_mirmachine(job_object):
    Path("data/yamls").mkdir(parents=True, exist_ok=True)
    Path("data/temp").mkdir(parents=True, exist_ok=True)
    gen_file_path = 'data/temp/' + job_object.species + '.txt'
    genome_file = open(gen_file_path, 'x')
    genome_file.write(job_object.data)
    genome_file.close()

    both_ways = ''  # "--add-all-nodes" if arguments["--add-all-nodes"] else ""
    dry_run = ''  # "-n" if arguments["--dry"] else ""
    unlock = ''  # "--unlock" if arguments["--unlock"] else ""
    remove = ''  # "--delete-all-output" if arguments["--remove"] else ""
    default_node_argument = "" if job_object.single_node else "| while read i; do mirmachine_tree_parser.py {meta_directory}/tree.newick $i {both_ways}; done".format(
        meta_directory=meta_directory, both_ways=both_ways)

    if job_object.single_fam_mode:
        yaml_argument = """echo {family} | awk -v genome={genome} -v species={species} 'BEGIN{{print "genome: "genome;print "species: "species;print "node: "node; print "mirnas:"}}{{print " - "$1}}' > data/yamls/{species}.yaml""".format(
            family=job_object.family,
            species=job_object.species,
            genome=gen_file_path)

    else:
        yaml_argument = """echo {node} {default_node_argument} | sort | uniq | while read a; \
        do grep $a {meta_directory}/nodes_mirnas_corrected.tsv; done \
        | grep -v NOVEL | grep -v NA | cut -f2 | sort | uniq | \
        awk -v genome={genome} -v species={species} -v node={node} 'BEGIN{{print "genome: "genome;print "species: "species;print "node: "node; print "mirnas:"}}{{print " - "$1}}' > data/yamls/{species}.yaml""".format(
            default_node_argument=default_node_argument,
            meta_directory=meta_directory,
            node=job_object.node,
            mirmachine_path=mirmachine_path,
            species=job_object.species,
            genome=job_object.data)

    subprocess.run(yaml_argument, check=True, capture_output=True, shell=True)
    sm_thread = threading.Thread(target=snakemake, daemon=True, args=('engine/mirmachine/workflows/mirmachine_search.smk',),
                                 kwargs={'config': {'meta_directory': meta_directory, 'model': job_object.model_type,
                                                    'mirmachine_path': mirmachine_path},
                                         'configfiles': ['data/yamls/' + job_object.species + '.yaml'],
                                         'printshellcmds': True, 'verbose': True,
                                         'summary': True, 'detailed_summary': True, 'force_incomplete': True})
    sm_thread.start()
    sm_thread.join()
    print('thread rejoined')
    # snakemake_argument="snakemake --rerun-incomplete {dry} {unlock} {remove} -j {cpu} -s {mirmachine_path}/workflows/mirmachine_search.smk --config meta_directory={meta_directory} model={model} mirmachine_path={mirmachine_path} --configfile=data/yamls/{species}.yaml".format(
    #    species=job_object.species,
    #    cpu=1,
    #    model=job_object.model_type,
    #    meta_directory=meta_directory,
    #    mirmachine_path=mirmachine_path,
    #    dry=dry_run,
    #    unlock=unlock,
    #    remove=remove)

    # subprocess.run(snakemake_argument, capture_output=True, shell=True)
