
from anytree import Node


class NodeWithData(Node):

    @classmethod
    def new_node(cls, name, parent=None, **kwargs):
        return cls(name, parent, **kwargs)

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

    def set_url(self, url):
        self.update_data('url', url)

    def get_topic(self):
        return self.get_data('topic')

    def get_url(self):
        return self.get_data('url')

    def set_note(self, notes):
        self.update_data('notes', notes)

    def get_note(self):
        return self.get_data('notes')
