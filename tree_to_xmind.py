
from xmind_builder import XMindBuilder

from product_tree import build_sample_tree, print_pretty_tree


def main():

    root_tree_node = build_sample_tree()
    root_tree_node.parent = None

    xmb = XMindBuilder("products.xmind", 'High Power')

    xmb.build_from_tree(root_tree_node)

    print_pretty_tree(root_tree_node)

    xmb.save("products.xmind")


if __name__ == "__main__":
    main()