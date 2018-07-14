from anytree import RenderTree


def print_pretty_tree(root_node):

    for pre, fill, node in RenderTree(root_node):
        print("{0} {1}".format(pre, node.name))


def print_tree(root_node):
    print(RenderTree(root_node))
