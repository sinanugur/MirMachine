import os


def import_all_families():
    families = []

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, '../engine/mirmachine/meta/cutoffs/combined/mirmachine_trusted_cutoffs.tsv')
    _file = open(file_path, 'r')
    # skip first line
    _file.readline()
    line = _file.readline()
    while line != '':
        family = line.split('\t')[0]
        families.append({'name': family})
        line = _file.readline()

    _file.close()
    return families
