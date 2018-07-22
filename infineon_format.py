

import re


def format_annotation_for_ifx(col_name, value):

    string = re.sub('<sub>', '_', col_name)
    string = re.sub('</sub>', '', string)

    return "{0}: {1}".format(string, value)
