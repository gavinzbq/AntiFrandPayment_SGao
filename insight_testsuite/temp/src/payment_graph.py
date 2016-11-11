#!/usr/bin/python -tt

""" 
Represent the previous payment network by graph, the most efficient data structure for 
graphs in Python is a dict of sets.
"""

from collections import defaultdict

class Graph(object):
    """ Graph data structure, undirected by default. """
    
    # add a 'directed' parameter to indicate if the connection is an arc or edge
    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)
    
    # Add connections (list of tuple pairs) to graph
    def add_connections(self, connections):

        for node1, node2 in connections:
            self.add(node1, node2)

    # Add connection between node1 and node2
    def add(self, node1, node2):

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    # Is node1 directly connected to node2
    def is_connected(self, node1, node2):
        
        return node1 in self._graph and node2 in self._graph[node1]


    # Find paths whose length is less or equal to 'max_len'; 
    # Feature 1: path length equals 2
    def find_feature1_path(self, node1, node2, path=[], max_len = 2):
        if len(path) >= max_len:
            return None
        path = path + [node1]
        if node1 == node2:
            return path
        if (node1 not in self._graph) or (node2 not in self._graph):
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_feature1_path(node, node2, path, max_len = max_len)
                if new_path:
                    return new_path
        return None
    
    #  Feature 2: find path whose length is less or equal to 3
    def find_feature2_path(self, node1, node2, path=[], max_len = 3):
        if len(path) >= max_len:
            return None
        path = path + [node1]
        if node1 == node2:
            return path
        if (node1 not in self._graph) or (node2 not in self._graph):
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_feature2_path(node, node2, path, max_len = max_len)
                if new_path:
                    return new_path
        return None
    
    #  Feature 3: find path whose length is less or equal to 5
    def find_feature3_path(self, node1, node2, path=[], max_len = 5):
        if len(path) >= max_len:
            return None
        path = path + [node1]
        if node1 == node2:
            return path
        if (node1 not in self._graph) or (node2 not in self._graph):
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_feature3_path(node, node2, path, max_len = max_len)
                if new_path:
                    return new_path
        return None

    
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))