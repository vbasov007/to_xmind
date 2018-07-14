
from anytree import Node


class NodeWithData(Node):

    def update_data(self, name, obj):
        self.__dict__.update({name: obj})

    def get_data(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return None

class XMindNode(NodeWithData):
    def set_topic(self, topic):
        self.update_data('topic', topic)
    def get_topic(self):
        return self.get_data('topic')