
from command_line_proc import turn_to_list
from product_tree import table_headers_dict, arg_to_header, table_to_tree, parameter_names_tree
from command_line_proc import parse_filter_arguments
from data_prefilter import include_only_data, exclude_data, include_if_match_string
from tree_node import XMindNode
from html_template import ProductTableOnly
from html_builder import make_html


def product_table_to_html(df,
                          category,
                          subcategory,
                          view_name,
                          main_topic,
                          tree_attributes,
                          part_attributes,
                          url_source,
                          exclude,
                          include_only,
                          match):

    a_tree_levels = turn_to_list(tree_attributes.split())
    a_annotations = turn_to_list(part_attributes.split())

    a_main_topic_name = main_topic

    a_url_col = url_source

    a_include_only = []
    a_exclude = []
    a_match = []

    if len(include_only) > 0:
        a_include_only = include_only.split(';')

    if len(exclude) > 0:
        a_exclude = exclude.split(';')

    if len(match) > 0:
        a_match = match.split(';')

    print("a_tree_levels:", a_tree_levels)
    print("a_annotations:", a_annotations)
    print("a_main_topic_name:", a_main_topic_name)
    print("a_include_only:", a_include_only)
    print("a_exclude:", a_exclude)
    print("a_match:", a_match)

    df = df.astype(str)

    header_dict = table_headers_dict(df)
    header_list = df.columns.values.tolist()

    for a in a_include_only:
        col, val = parse_filter_arguments(a)
        df = include_only_data(df, arg_to_header(col, header_dict, header_list), val)

    for a in a_exclude:
        col, val = parse_filter_arguments(a)
        df = exclude_data(df, arg_to_header(col, header_dict, header_list), val)

    if a_match:
        col, val = parse_filter_arguments(a_match)
        df = include_if_match_string(df, arg_to_header(col, header_dict, header_list), val[0])

    root_node = XMindNode(a_main_topic_name)

    tree_levels = [arg_to_header(a, header_dict, header_list) for a in a_tree_levels]
    tree_levels = [a for a in tree_levels if a]

    parameter_names_tree(tree_levels, root_node)

    anns = [arg_to_header(a, header_dict, header_list) for a in a_annotations]
    anns = [a for a in anns if a]

    url_col = arg_to_header(a_url_col, header_dict, header_list)

    notes = []

    table_to_tree(
        df,
        tree_levels,
        root_node,
        anns,
        notes,
        last_level_url_col_name=url_col,
        html_mode=True)

    html_data = make_html(
            root_node,
            ProductTableOnly,
            category=category,
            subcategory=subcategory,
            view_name=view_name)

    return html_data