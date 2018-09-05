

from tree_node import XMindNode


def tree_to_html_list(root_node: XMindNode):

    child_html = ""
    for node in root_node.children:
        child_html += tree_to_html_list(node)

    href = root_node.get_url()

    if not href:
        href = '#'

    if len(child_html) > 0:
        return '<li><a href="{0}">{1}</a><ul>{2}</ul></li>'.format(href, root_node.name, child_html)
    else:
        return '<li><a href="{0}">{1}</a></li>'.format(href, root_node.name)


def make_html(root_node: XMindNode, template, category='', subcategory='', view_name=''):

    page_title = root_node.name

    table_headers_html = ""
    table_content = ""
    for node in root_node.children:
        table_headers_html += '<th>{0}</th>'.format(node.name)
        h = ""
        for sub_node in node.children:
            h += tree_to_html_list(sub_node)

        table_content += '<td class="nowrap"><ul class="tree">{0}</ul></td>'.format(h)

    return template().make(
        Category=category,
        Subcategory=subcategory,
        View_Name=view_name,
        Page_Title=page_title,
        Table_Title=page_title,
        Table_Headers=table_headers_html,
        Table_Content=table_content,
        )

