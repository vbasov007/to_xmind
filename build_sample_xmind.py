import os
import pandas as pd
from tree_node import XMindNode
from product_tree import table_to_tree, variations
from print_tree import print_pretty_tree

from xmind_builder import XMindBuilder

def build_sample_tree():

    dirpath = os.getcwd()
    df = pd.read_excel(dirpath + '\datafiles\products.xlsx')

    for col in df.columns.tolist():
        print("{0}: {1}".format(col, len(variations(df, col))))

    order = ['Configuration', 'Voltage Class', 'Current', 'Housing', 'Product']

    ann = ['Technology', 'Features', 'Product Status', 'Qualification']

    root = XMindNode('IGBT Module')

    table_to_tree(df, order, root, ann, node_class=root.__class__)

    print_pretty_tree(root)

    root_tree_node = root
    root_tree_node.parent = None

    xmb = XMindBuilder("products.xmind", 'High Power')

    xmb.build_from_tree(root_tree_node)

    xmb.save("products.xmind")


if __name__ == "__main__":
    build_sample_tree()
