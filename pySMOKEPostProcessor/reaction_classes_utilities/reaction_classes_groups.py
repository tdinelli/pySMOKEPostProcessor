# TODO MOVE ALL USEFUL FUNCTIONS IN JUST ONE FILE.
"""
Description: reads file with rxn class groups and groups them in a dictionary
"""
from ..amech_utils import pathtools
from ..amech_utils import ptt

def ReadReactionsGroups(filepath):
    rxngroups_str = pathtools.read_file(filepath, remove_comments = '#', remove_whitespace=True)

    """ 
    Read reaction groups
    return group and subclass dictionary:
    grp_dct = {'classgroup': [subclass1, subclass2, ..]}
    subclass_dct = {'subclass' : 'classgroup' }
    equivalent but easier handling
    """

    grp_blocks = ptt.named_end_blocks(rxngroups_str, 'classtype', footer='classtype')
    grp_dct = ptt.keyword_dcts_from_blocks(grp_blocks)

    # make a dct subclass: classtype
    subclass_dct = {}
    for key, val in grp_dct.items():
        for subclass in val:
            subclass_dct[subclass] = key

    return grp_dct, subclass_dct
