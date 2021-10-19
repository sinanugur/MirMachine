import os


def get_and_parse_results(tag):
    base_dir = os.path.dirname(__file__)
    result_dir = os.path.join(base_dir, '../../engine/results/predictions/')
    file_paths = ['fasta/{tag}.PRE.fasta'.format(tag=tag), 'filtered_gff/{tag}.PRE.gff'.format(tag=tag),
                  'heatmap/{tag}.heatmap.tsv'.format(tag=tag)]
    contents = []
    for path in file_paths:
        file = open(os.path.join(result_dir, path), 'r')
        content = file.read()
        contents.append(content)
        file.close()
    content_dict = {'fasta': contents[0],
                    'filtered_gff': contents[1],
                    'heatmap': contents[2]}
    return content_dict
