import os
import zipfile
from django.http import HttpResponse
from ..models import Job


def get_and_parse_results(tag):
    file_paths = get_result_paths(tag)
    contents = []
    for path in file_paths:
        file = open(path, 'r')
        content = file.read()
        contents.append(content)
        file.close()
    content_dict = {'fasta': contents[0],
                    'filtered_gff': contents[1],
                    'heatmap': contents[2]}
    return content_dict


def get_result_paths(tag, get_result_dir_and_relative=False):
    base_dir = os.path.dirname(__file__)
    result_dir = os.path.join(base_dir, '../../engine/results/predictions/')
    file_paths = ['fasta/{tag}.PRE.fasta'.format(tag=tag), 'filtered_gff/{tag}.PRE.gff'.format(tag=tag),
                  'heatmap/{tag}.heatmap.tsv'.format(tag=tag)]
    if get_result_dir_and_relative:
        return file_paths, result_dir
    return [os.path.join(result_dir, x) for x in file_paths]


def zip_results(tag):
    file_paths, result_dir = get_result_paths(tag, get_result_dir_and_relative=True)
    file_paths.append('gff/{}.PRE.gff'.format(tag))
    generate_meta_data(tag)
    file_paths.append('{}_meta.txt'.format(tag))
    os.chdir(result_dir)
    response = HttpResponse(content_type='application/zip')
    zip_file = zipfile.ZipFile(response, 'w')
    for full in file_paths:
        zip_file.write(full)
    response['Content-Disposition'] = 'attachment; filename={}_results.zip'.format(tag)
    zip_file.close()
    return response


def generate_meta_data(tag):
    job_object = Job.objects.get(species=tag)
    base_dir = os.path.dirname(__file__)
    meta_file_path = os.path.join(base_dir, '../../engine/results/predictions/{tag}_meta.txt'.format(tag=tag))
    meta_file = open(meta_file_path, 'x')
    parameters = {'id': 'ID', 'submitted': 'Submitted', 'initiated': 'Initiated', 'completed': 'Completed', 'hash': 'Dataset hash', 'species': 'Species', 'model_type': 'Model Type', 'node': 'Node', 'single_fam_mode': 'Single Family Mode', 'single_node': 'Single node'}
    for _key in parameters.keys():
        param = getattr(job_object, _key)
        meta_file.write(parameters[_key] + ':\t' + str(param) + '\n')
    meta_file.close()