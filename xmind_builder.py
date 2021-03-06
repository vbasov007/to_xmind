
import re
import xmind

from tree_node import XMindNode


def is_same_title(title1, title2):

    t1 = re.sub('[^A-Za-z0-9]+', '', title1)
    t2 = re.sub('[^A-Za-z0-9]+', '', title2)

    return t1 == t2


def already_existing_topic(node):
    existing_topics = node.parent.get_topic().getSubTopics()
    for t in existing_topics:
        if is_same_title(t.getTitle(), node.name):
            return t
    return None


def add_subtopic_from_node(node):

    t = already_existing_topic(node)
    if t is not None:
        node.set_topic(t)
    else:
        new_topic = node.parent.get_topic().addSubTopic()
        new_topic.setTitle(node.name)
        new_topic.setFolded()

        if node.get_url():
            new_topic.setURLHyperlink(node.get_url())

        if node.get_note():
            new_topic.setPlainNotes(node.get_note())

        node.set_topic(new_topic)


def setup_central_topic(root_node, xmind_central_topic):
    xmind_central_topic.setTitle(root_node.name)
    root_node.set_topic(xmind_central_topic)
    if root_node.get_url():
        xmind_central_topic.setURLHyperlink(root_node.get_url())


class XMindBuilder:

    def __init__(self, file_name, central_topic_name=None, sheet_name=None):
        self.workbook = xmind.load(file_name)
        self.sheet = self.workbook.getPrimarySheet()
        if sheet_name:
            self.sheet.setTitle(sheet_name)

        self.central_topic = self.sheet.getRootTopic()

        if central_topic_name:
            self.central_topic.setTitle(central_topic_name)

        self.central_topic_tree_node = XMindNode(
            self.central_topic.getTitle(),
            parent=None,
            topic=self.central_topic)

    def build_from_tree(self, root_node, xmind_central_topic=None):

        if xmind_central_topic:
            setup_central_topic(root_node, xmind_central_topic)
        else:
            add_subtopic_from_node(root_node)

        for node in root_node.descendants:
            add_subtopic_from_node(node)

    def save(self, file_name):
        xmind.save(self.workbook, file_name)