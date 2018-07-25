"""
Usage:
    to_xmind FILE_XLSX (-i)
    to_xmind FILE_XLSX [--xmind=FILE_XMIND] [--tree=COL_HEADS]... [--ann=ANN_COL_HEADS]... [--note=NOTE_COL_HEADS]...
                        [--sheet=SHEET] [--main=TOPIC] [--url=URL_COL] [-i] [-p]
                        [--include_only=INCL_FLT_STR]... [--exclude=EXCL_FLT_STR]...
                        [--match=MATCH_STR]  [-comment=COMMENT]
        
Arguments:
    FILE_XLSX       Input excel file path
    COL_HEADS       Columns used to build tree
    URL_COL         Column with URL for datasheet
    ANN_COL_HEADS   Columns used to annotate last value in a tree
    FILE_XMIND      Output .xmind file path
    SHEET           Optional .xmind workbook sheet name
    TOPIC           Name of root topic
    COMMENT         Any comment to command line string
    
Options:
    -h --help
    -i --info                       .xlsx file info, tree info
    -t --tree=COL_HEADS             Next column name to build tree
    -u --url=URL_COL                Take URL from this column
    -n --note=NOTE_COL_HEADS        Next columns to note the deepest value in a tree
    -a --ann=ANN_COL_HEADS          Next columns to annotate the deepest value in a tree
    -x --xmind=FILE_XMIND           XMIND file path
    -s --sheet=SHEET                Optional xmind sheet name
    -m --main=TOPIC                    Optional xmind root topic [default: MAIN]
    -p --print                      Print generated tree on console
    -o --include_only=INCL_FLT_STR
    -e --exclude=EXCL_FLT_STR
    --match=MATCH_STR


"""

from docopt import docopt
from product_tree import print_header_value_variation_stat, print_all_variations, table_headers_dict, table_to_tree, arg_to_header
from print_tree import print_pretty_tree, print_pretty_tree_plan
import pandas as pd
from tree_node import XMindNode
from xmind_builder import XMindBuilder
from data_prefilter import parse_filter_arguments, include_only_data, exclude_data, include_if_match_string
import sys
from mylogger import mylog

def to_xmind():
    args = docopt(__doc__)

    mylog.debug(sys.argv)
    mylog.debug(args)

    a_info = args['--info']
    a_tree_levels = args['--tree']
    a_annotations = args['--ann']
    a_notes = args['--note']
    a_print = args['--print']
    a_file_xlsx = args['FILE_XLSX']
    a_file_xmind = args['--xmind']
    a_main_topic_name = args['--main']
    a_url_col = args['--url']
    a_include_only = args['--include_only']
    a_exclude = args['--exclude']
    a_match = args['--match']

    try:
        df = pd.read_excel(a_file_xlsx)
    except:
        mylog.error("Can't read file: {0}".format(a_file_xlsx))
        return

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
    if len(tree_levels) > 1:
        anns = [arg_to_header(a, header_dict, header_list) for a in a_annotations]
        anns = [a for a in anns if a]

        notes = [arg_to_header(a, header_dict, header_list) for a in a_notes]
        notes = [a for a in notes if a]

        url_col = arg_to_header(a_url_col, header_dict, header_list)

        if a_info:
            print_pretty_tree_plan(tree_levels, anns, notes, url_col)

        table_to_tree(
            df, tree_levels, root_node,
            anns, notes,
            last_level_url_col_name=url_col, node_class=root_node.__class__)

    if a_info:
        print_header_value_variation_stat(df)

        # if a_tree_levels:
        #    for v in a_tree_levels:
        #        print_all_variations(df, v, header_dict=header_dict, max_items=5)

    if a_print:
        print_pretty_tree(root_node, 30)

    if a_file_xmind:
        xmb = XMindBuilder(a_file_xmind)
        print('File "{0}" will be overwritten, data can be lost!'.format(a_file_xmind))
        answer = input('Type "yes" if agree >>>')
        if answer == 'yes':
            root_node.parent = xmb.central_topic_tree_node
            xmb.build_from_tree(root_node, xmind_central_topic=xmb.central_topic)
            xmb.save(a_file_xmind)
            print('XMIND saved to file "{0}"'.format(a_file_xmind))
        else:
            print('Quited without saving. File was not changed')



if __name__ == '__main__':
    to_xmind()


