import os


def import_all_families():
    families = []
    protostomes = get_strings_in_files('proto')
    deuterostomes = get_strings_in_files('deutero')

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, '../engine/mirmachine/meta/cutoffs/combined/mirmachine_trusted_cutoffs.tsv')
    _file = open(file_path, 'r')
    # skip first line
    _file.readline()
    line = _file.readline()
    while line != '':
        family = line.split('\t')[0]
        proto = family in protostomes
        deutero = family in deuterostomes
        families.append({
            'name': family,
            'proto': proto,
            'deutero': deutero
        })
        line = _file.readline()

    _file.close()
    return families


def get_strings_in_files(type):
    elems = []
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, '../engine/mirmachine/meta/cutoffs/' + type + '/mirmachine_trusted_cutoffs.tsv')
    _file = open(file_path, 'r')
    _file.readline()
    line = _file.readline()
    while line != '':
        family = line.split('\t')[0]
        elems.append(family)
        line = _file.readline()
    _file.close()
    return elems


def import_node_to_family_db():
    relations = []
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, '../engine/mirmachine/meta/nodes_mirnas_corrected.tsv')
    _file = open(file_path, 'r')
    line = _file.readline()
    while line != '':
        elems = line.split('\t')
        if 'NOVEL' not in elems[1]:
            relations.append({
                'node': elems[0],
                'family': elems[1].strip()
            })
        line = _file.readline()
    _file.close()
    return relations