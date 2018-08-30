
from anytree import Node


def tree_to_html_list(root_node: Node):

    child_html = ""
    for node in root_node.children:
        child_html += tree_to_html_list(node)

    if len(child_html) > 0:
        return '<li><a href="#">{0}</a><ul>{1}</ul></li>'.format(root_node.name, child_html)
    else:
        return '<li><a href="#">{0}</a></li>'.format(root_node.name)


def  make_html(root_node: Node, template):

    page_title = root_node.name

    table_headers_html = ""
    table_content = ""
    for node in root_node.children:
        table_headers_html += '<th>{0}</th>'.format(node.name)
        h = ""
        for sub_node in node.children:
            h += tree_to_html_list(sub_node)

        table_content += '<td><ul class="tree">{0}</ul></td>'.format(h)

    return template.html.substitute(
        Page_Title=page_title,
        Table_Headers=table_headers_html,
        Table_Content=table_content,
        Script=template.script,
        Style=template.style,)

