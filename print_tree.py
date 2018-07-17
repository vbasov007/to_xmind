from anytree import RenderTree


def print_pretty_tree(root_node, max_nodes=0):

    if max_nodes == 0:
        for pre, fill, node in RenderTree(root_node):
            print("{0}{1}".format(pre, node.name))
    else:
        count = 0
        for pre, fill, node in RenderTree(root_node):
            print("{0}{1}".format(pre, node.name))
            count += 1
            if count > max_nodes:
                print('\n.\n.\n.\n')
                break



def print_tree(root_node):
    print(RenderTree(root_node))
