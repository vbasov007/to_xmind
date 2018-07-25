from anytree import RenderTree, Node


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

def print_pretty_tree_plan(tree_levels, annotation_list=None, notes_list=None, url_col=None):

    print("--------------------TREE PLAN:---------------------")

    root = Node('"{0}"'.format(tree_levels[0]))
    prev_node = root
    for level in tree_levels[1:]:
        new_node = Node('"{0}"'.format(level), parent=prev_node)
        prev_node = new_node

    print_pretty_tree(root)

    if annotation_list:
        print('Annotations: "{0}"'.format(", ".join(annotation_list)))

    if notes_list:
        print('Pop-up notes: "{0}"'.format(", ".join(notes_list)))

    if url_col:
        print('Url link source: "{0}"'.format(url_col))
    print("------------------------END------------------------")

def print_tree(root_node):
    print(RenderTree(root_node))
