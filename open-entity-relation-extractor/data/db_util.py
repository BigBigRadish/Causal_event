# -*- coding: utf-8 -*-
'''
Created on 2019年03月04日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
from py2neo import Graph, Node, Relationship
import json
from tqdm import tqdm

# graph = Graph(
#             "http://localhost:11003",
#              username="neo4j",
#              password="123456"
#         )


class NeoManager:
    def __init__(self, host='http://10.214.193.166:7474', username="neo4j", password="123456"):
        self.graph = Graph(host, username=username, password=password)
        self.entity2node = dict([(n['name'], n) for n in self.graph.nodes.match()])

    def get_node(self, entity_name, tp):
        node = self.entity2node.get(entity_name, None)
        if node is None:
            node = Node(tp, name=entity_name)
            try:
                self.graph.create(node)
            except Exception as e:
                pass
        self.entity2node.setdefault(entity_name, node)
        return node

    def write2db(self, data):
        for item in tqdm(data):
            triplet = item['triplet']
            entity1 = ''.join(triplet['entity1'])
            entity2 = ''.join(triplet['entity2'])
            relation = ''.join(triplet['relation'])
            node1 = self.get_node(entity1, triplet['type1'])
            node2 = self.get_node(entity2, triplet['type2'])
            if relation.strip() == '':
                label = Relationship(node1, node2)
            else:
                label = Relationship(node1, relation, node2)
            try:
                self.graph.create(label)
            except Exception as e:
                pass

    def clear(self):
        self.graph.delete_all()
        self.entity2node = {}


if __name__ == '__main__':
    db_manager = NeoManager()
    db_manager.clear()
    with open('data/output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        db_manager.write2db(data)





