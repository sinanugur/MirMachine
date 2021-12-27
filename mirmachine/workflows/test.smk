

from collections import defaultdict
import os.path
from yaml import load

from mirmachine import meta
from mirmachine import workflows
import mirmachine
mirmachine_path=os.path.dirname(mirmachine.__file__)

meta_directory=os.path.dirname(meta.__file__)


model=config.get('model','combined')
#meta_directory=config.get('meta_directory','meta')
mirnas=[x.title() + ".PRE" for x in config['mirnas']]



rule search_CM:
    input:
        expand(meta_directory + "/cms/" + model + "/{mirna}.CM",mirna=mirnas)
