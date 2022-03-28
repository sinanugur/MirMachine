import datetime
import os
from django.utils import timezone
from ..models import Job
from MirMachineWebapp import user_config as config
from .result_parser import get_result_paths


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


def delete_job_data(job_object):
    _id = job_object.id
    species_tag = job_object.species
    print('Deleting results and DB entry for job with id {}'.format(str(_id)))
    paths, result_dir = get_result_paths(species_tag, True)

    for path in paths:
        file = os.path.join(result_dir, path)
        if os.path.exists(file):
            os.remove(file)

    file = os.path.join(result_dir, '{species}_meta.txt'.format(species=species_tag))
    if os.path.exists(file):
        os.remove(file)
    # Delete input files
    if job_object.mode == 'file':
        input_dir = 'media/uploads'
        file = os.path.join(input_dir, '{id}.txt'.format(id=job_object.id))
        if os.path.exists(file):
            os.remove(file)
        file = os.path.join(input_dir, '{id}.txt.fai'.format(id=job_object.id))
        if os.path.exists(file):
            os.remove(file)
    if job_object.mode == 'accNum':
        jobs = Job.objects.filter(data=job_object.data)
        if jobs.count() <= 1: #check if multiple jobs use the same dataset
            file = job_object.data
            if os.path.exists(file):
                os.remove(file)
            file = job_object.data + '.fai'
            if os.path.exists(file):
                os.remove(file)
    job_object.delete()


def delete_expired_jobs():
    jobs = Job.objects.all().order_by('initiated')
    for job in jobs:
        if has_expired(job):
            delete_job_data(job)
        else:
            return


def has_expired(job_object):
    expiration_threshold = timezone.localtime(timezone.now()) - datetime.timedelta(days=config.JOB_EXPIRATION_TIME)
    return job_object.initiated < expiration_threshold
