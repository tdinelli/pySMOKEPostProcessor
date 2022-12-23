"""
Rxn class groups
"""

import sys
import numpy as np

from pySMOKEPostProcessor.amech_utils import pathtools
from pySMOKEPostProcessor.amech_utils import ptt
# reads file with rxn class groups and groups them in a dictionary

def ReadRxnGroups(path, filename):
    rxngroups_str = pathtools.read_file(path, filename, remove_comments = '#', remove_whitespace=True)

    """ Parse the auxiliary file to handleget the info from the file

        out dict[(pes_grp_idx_lst] = pes_grp_params
        where params read from input and
        pes_grp_idx_lst = {{pes_idx1, subpes_idx1}, ...}
    """

    grp_blocks = ptt.named_end_blocks(
        rxngroups_str, 'classtype', footer='classtype')
    grp_dct = ptt.keyword_dcts_from_blocks(grp_blocks)

    # make a dct subclass: classtype
    subclass_dct = {}
    for key, val in grp_dct.items():
        for subclass in val:
            subclass_dct[subclass] = key

    return grp_dct, subclass_dct
