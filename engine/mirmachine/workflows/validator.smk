import os.path


mirmachine_path=os.path.dirname(config['mirmachine_path'])

meta_directory=os.path.dirname(config['meta_directory'])


model=config.get('model','combined')

mirnas=[x.title() + ".PRE" for x in config['mirnas']]


rule search_CM:
    input:
         expand(meta_directory + "/cms/" + model + "/{mirna}.CM",mirna=mirnas)