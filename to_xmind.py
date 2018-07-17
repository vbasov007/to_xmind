"""
Usage:
    to_xmind FILE_XLSX (-i)
    to_xmind FILE_XLSX [--xmind=FILE_XMIND] [--tree=COL_HEADS]... [--ann=ANN_COL_HEADS]... [--sheet=SHEET] [--main=TOPIC] [-o|-u|-i] [-p]
        
Arguments:
    FILE_XLSX       Input excel file path
    COL_HEADS       Columns used to build tree
    ANN_COL_HEADS   Columns used to annotate last value in a tree
    FILE_XMIND      Output .xmind file path
    SHEET           Optional .xmind workbook sheet name
    TOPIC           Name of root topic
    
Options:
    -h --help
    -i --info               .xlsx file info, tree info
    -t --tree=COL_HEADS     Next column name to build tree
    -a --ann=ANN_COL_HEADS  Next columns to annotate the deepest value in a tree
    -x --xmind=FILE_XMIND   XMIND file path
    -o --overwrite          Overwrite xmind file. All old data will be lost
    -u --update             Update xmind file. The xmind file will be updated with new topics
    -s --sheet=SHEET        Optional xmind sheet name
    -m --main=TOPIC         Optional xmind root topic [default: MAIN]
    -p --print              Print generated tree on console

"""

from docopt import docopt
from product_tree import print_header_value_variation_stat, print_all_variations, table_headers_dict, table_to_tree, arg_to_header
from print_tree import print_pretty_tree, print_pretty_tree_plan
import pandas as pd
from tree_node import XMindNode
from xmind_builder import XMindBuilder

def to_xmind():
    args = docopt(__doc__)
    # print(args)

    a_info = args['--info']
    a_tree_levels = args['--tree']
    a_annotations = args['--ann']
    a_print = args['--print']
    a_file_xlsx = args['FILE_XLSX']
    a_file_xmind = args['--xmind']
    a_main_topic_name = args['--main']

    try:
        df = pd.read_excel(a_file_xlsx)
    except:
        print("Can't read file: {0}".format(a_file_xlsx))
        return

    header_dict = table_headers_dict(df)
    header_list = df.columns.values.tolist()

    root_node = XMindNode(a_main_topic_name)

    tree_levels = [arg_to_header(a, header_dict, header_list) for a in a_tree_levels]
    tree_levels = [a for a in tree_levels if a]
    if len(tree_levels) > 1:
        anns = [arg_to_header(a, header_dict, header_list) for a in a_annotations]
        anns = [a for a in anns if a]
        if a_info:
            print_pretty_tree_plan(tree_levels, anns)
        table_to_tree(df, tree_levels, root_node, anns, root_node.__class__)

    if a_info:
        print_header_value_variation_stat(df)


        if a_tree_levels:
            for v in a_tree_levels:
                print_all_variations(df, v, header_dict=header_dict, max_items=5)

    if a_print:
        print_pretty_tree(root_node, 30)

    if a_file_xmind:
        xmb = XMindBuilder(a_file_xmind)
        print('File "{0}" will be overwritten, data can be lost!'.format(a_file_xmind))
        answer = input('Type "yes" if agree >>>')
        if answer == 'yes':
            xmb.build_from_tree(root_node)
            xmb.save(a_file_xmind)
            print('XMIND saved to file "{0}"'.format(a_file_xmind))
        else:
            print('Quited without saving. File was not changed')



if __name__ == '__main__':
    to_xmind()


