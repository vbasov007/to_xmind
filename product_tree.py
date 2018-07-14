import pandas as pd
from anytree import Node
import re


def parameter_sort_key(str):

    r = re.match(r"^[\d]+\.?[\d]*", str)

    try:
        res = r.group(0)
        return float(res)
    except AttributeError:
        return 999999

def variations(df, col_header):
    a = set(df[col_header].tolist())
    res = list(map(str, list(a)))
    res.sort()
    res.sort(key=lambda x: parameter_sort_key(x))
    return res


def take_only(df, col_name, value):
    return df[df[col_name] == value]


def annotations(df, info_col_names):
    data = df[info_col_names]

    out_list = data.values.tolist()
    out = out_list[0]

    out = [re.sub('[ \t]+', ' ', s) for s in out if not pd.isna(s)]

    return out



def table_to_tree(df, tree_level_names, parent_node, last_level_annotations, node_class=Node):
    if df.empty:
        return

    conditions = variations(df, tree_level_names[0])
    for c in conditions:
        if pd.isna(c):
            continue

        filtered_df = take_only(df, tree_level_names[0], c)

        if len(tree_level_names) > 1:
            new_node = node_class(c, parent_node)
            table_to_tree(filtered_df, tree_level_names[1:], new_node, last_level_annotations, node_class=node_class)
        else:
            annot = ""
            if len(last_level_annotations) > 0:
                annot = ": " + ", ".join(annotations(filtered_df, last_level_annotations))
                node_class(c + annot, parent_node)

    return

