import pandas as pd
from anytree import Node
import re

from infineon_format import format_annotation_for_ifx

from tree_node import XMindNode

from validators import url as is_url

def parameter_sort_key(string):

    r = re.match(r"^[-]?[\d]+\.?[\d]*", string)

    try:
        res = r.group(0)
        return float(res)
    except AttributeError:
        return 9999999


def is_sortable_as_number(string):

    r = re.match(r"^[-]?[\d]+\.?[\d]*", string)
    try:
        r.group(0)
        return True
    except AttributeError:
        return False


def sorted_smart(lst):
    as_number = [s for s in lst if is_sortable_as_number(s)]
    as_string = [s for s in lst if not is_sortable_as_number(s) and s != '-']

    as_number.sort(key=lambda x: parameter_sort_key(x))
    as_string.sort()

    if '-' in lst:
        as_string += '-'

    return as_number + as_string

def variations(df, col_header):
    a = set(df[col_header].tolist())
    lst = list(a)
    lst = [x if not pd.isna(x) else '-' for x in lst]
    res = list(map(str, lst))

    res = sorted_smart(res)

    return res


def take_only(df, col_name, value):
    return df[df[col_name] == value]


def annotations(df, info_col_names):
    data = df[info_col_names]

    out_list = data.values.tolist()
    out = out_list[0]

    out = [re.sub('[ \t]+', ' ', s) for s in out if not pd.isna(s)]

    return out

def annotations_with_title(df, info_col_names):

    data = df[info_col_names]

    out = []
    for col in data:
        val = data[col].values.tolist()[0]
        if val != "-":
            annot = format_annotation_for_ifx(col, val)
            out.append(annot)

    return out

def get_single_col_value(df, col_name):
    return df[col_name].values.tolist()[0]

def format_multiline_annot(ann_list, max_string_len = 50):
    res = ''
    cur_str_len = 0
    for ann in ann_list:
        if cur_str_len + len(ann) + 3 > max_string_len:
            res += '\n' + ann
            cur_str_len = len(ann)
        else:
            if cur_str_len == 0:
                res += ann
                cur_str_len = len(ann)
            else:
                res += ' - ' + ann
                cur_str_len += len(ann) + 3

    return res



def table_to_tree(
        df, tree_level_names, parent_node,
        last_level_annotations,
        pop_up_notes,
        last_level_url_col_name=None,
        node_class=XMindNode):

    if df.empty:
        return

    conditions = variations(df, tree_level_names[0])
    for c in conditions:
        if pd.isna(c):
            continue

        filtered_df = take_only(df, tree_level_names[0], c)

        if len(tree_level_names) > 1:
            new_node = node_class(c, parent_node)
            table_to_tree(
                filtered_df,
                tree_level_names[1:],
                new_node,
                last_level_annotations,
                pop_up_notes,
                last_level_url_col_name=last_level_url_col_name,
                node_class=node_class)
        else:
            ann_list = annotations_with_title(filtered_df, last_level_annotations)
            new_node = node_class("{0}\n{1}".format(c, format_multiline_annot(ann_list)), parent_node)

            pop_up_notes_list = annotations_with_title(filtered_df, pop_up_notes)
            new_node.set_note(format_multiline_annot(pop_up_notes_list))

            if last_level_url_col_name:
                url = get_single_col_value(filtered_df, last_level_url_col_name)
                if is_url(url):
                    new_node.set_url(url)

    return


def table_headers_dict(df):

    headers = df.columns.values.tolist()

    out_dict = dict()
    i = 1
    for h in headers:
        out_dict.update({str(i): str(h)})
        i += 1

    return out_dict


def arg_to_header(arg, header_dict, header_list):

    if arg in header_list:
        return arg
    elif arg in header_dict:
        return header_dict[arg]
    else:
        return None


def print_header_value_variation_stat(df):

    headers = df.columns.values.tolist()
    i = 1
    for h in headers:
        print('{0}. "{1}" - {2}'.format(i, h, len(variations(df, h))))
        i += 1


def print_all_variations(df, arg, header_dict=None, max_items = 999999):

    if header_dict:
        header = arg_to_header(arg, header_dict, df.columns.values.tolist())
    else:
        header = arg

    if header:
        lst = variations(df, header)
        if len(lst) > max_items:
            lst = lst[:max_items]
        print('\n"{0}":\n'.format(header))
        print('{0}'.format(repr(", ".join(lst))))
    else:
        print('\n"{0}" not found\n'.format(arg))
