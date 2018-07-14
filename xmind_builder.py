
import xmind

from tree_node import XMindNode


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

    @staticmethod
    def add_subtopic_from_node(node):

        new_topic = node.parent.get_topic().addSubTopic()
        new_topic.setTitle(node.name)
        node.set_topic(new_topic)

    def build_from_tree(self, root_node):

        if root_node.parent is None:
            root_node.parent = self.central_topic_tree_node

        self.add_subtopic_from_node(root_node)
        for node in root_node.descendants:
            self.add_subtopic_from_node(node)

    def save(self, file_name):
        xmind.save(self.workbook, file_name)