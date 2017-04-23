import logging
import copy
from data.python_templates.body_parts import body_part_templates


logger_ = logging.getLogger()


class BodypartTree(object):
    CONNECTION_TYPE_CENTER = 0
    CONNECTION_TYPE_ATTACHED = 1
    CONNECTION_TYPE_INSERTED = 2

    def __init__(self, central_node_name, central_body_part_uid):
        self.nodes = [BodypartTreeNode(central_node_name, central_body_part_uid, self.CONNECTION_TYPE_CENTER)]

    def copy(self):
        return copy.deepcopy(self)

    def attach(self, parent_node_name, children_node_name, children_body_part_uid):
        self._bind_new_child_to_parent(
            parent_node_name, children_node_name, children_body_part_uid, self.CONNECTION_TYPE_ATTACHED)

    def insert(self, parent_node_name, children_node_name, children_body_part_uid):
        self._bind_new_child_to_parent(
            parent_node_name, children_node_name, children_body_part_uid, self.CONNECTION_TYPE_INSERTED)

    def _bind_new_child_to_parent(self, parent_node_name, children_node_name, children_body_part_uid, connection_type):
        parent_node = next((node for node in self.nodes if node.name == parent_node_name), None)
        if parent_node:
            child_bodypart_node = BodypartTreeNode(children_node_name, children_body_part_uid, connection_type)
            parent_node.add_child_node(child_bodypart_node)
            self.nodes.append(child_bodypart_node)
        else:
            logger_.error("Tried to bind bodypart {} to non existing parent {}.".format(
                children_node_name, parent_node_name))


class BodypartTreeNode(object):
    def __init__(self, name, body_part_uid, connection_type):
        self.name = name
        self.body_part_uid = body_part_uid
        self.instance = body_part_templates[body_part_uid]
        self.connection_type = connection_type
        self.children_nodes = []

    def add_child_node(self, child_node):
        self.children_nodes.append(child_node)