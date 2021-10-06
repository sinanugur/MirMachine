import os
from ..models import Job


def clean_up_temporary_files():
    print('Cleaning up temporary files')
    base_dir = 'engine/'
    directory_list = ['data/genomes', 'data/temp', 'data/yamls']
    for directory in directory_list:
        cur_dir = base_dir + directory
        if os.path.exists(cur_dir):
            for filename in os.listdir(cur_dir):
                path_to_file = os.path.join(cur_dir, filename)
                print('\tRemoved: ' + path_to_file)
                os.remove(path_to_file)
    analyses_path = 'engine/analyses/output'
    if os.path.exists(analyses_path):
        for directory in os.listdir(analyses_path):
            directory_path = os.path.join(analyses_path, directory)
            if os.path.isdir(directory_path):
                for filename in os.listdir(directory_path):
                    path_to_file = os.path.join(directory_path, filename)
                    print('\tRemoved: ' + path_to_file)
                    os.remove(path_to_file)
                print('\tRemoved: ' + directory_path)
                os.rmdir(directory_path)


def delete_job_data(_id, species_tag):
    job_object = Job.objects.get(id=_id)
    job_object.delete()
    result_dir = 'engine/results/predictions'

    file = os.path.join(result_dir, '/fasta/{species}.PRE.fasta'.format(species=species_tag))
    if os.path.exists(file):
        os.remove(file)
    file = os.path.join(result_dir, '/filtered_gff/{species}.PRE.gff'.format(species=species_tag))
    if os.path.exists(file):
        os.remove(file)
    file = os.path.join(result_dir, '/gff/{species}.PRE.gff'.format(species=species_tag))
    if os.path.exists(file):
        os.remove(file)
    file = os.path.join(result_dir, '/heatmap/{species}.heatmap.tsv'.format(species=species_tag))
    if os.path.exists(file):
        os.remove(file)
