#!/usr/bin/python -tt

"""
Insight Data Engineering Fellowship Program, starting Jan. 2017 in New York City.
Coding Challenge: develop features to prevent fraudulent payment requests for PayMo. 

Shanyun Gao

"""
import sys
import csv
import os


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

    # Remove all references to node
    def remove(self, node):
        
        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

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
        if node1 not in self._graph:
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
        if node1 not in self._graph:
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
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_feature3_path(node, node2, path, max_len = max_len)
                if new_path:
                    return new_path
        return None

    
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))
        
        
def transfer_verify(filename1, filename2):
    """
    Import input csv files, store values of each header in columns with numerical index:
    time:0, id1:1, id2:2, amount:3, message:4
    Combine column[1] and [2] as a list of tuples: [('id1', 'id2'), then generate payment 
    network graph. The graph will be updated with incoming transfers (each line in 
    filename2).
    
    Use the exisiting payment network to verify each new transfer, based on graph theory.
    """  
    
    # Read filename1
    # Each value in each column is appended to a list   
    columns1 = defaultdict(list)
    
    with open(filename1, 'rU') as file1:
        reader1 = csv.reader(file1)
        reader1.next()
        for row in reader1:
            for (i,v) in enumerate(row):
                columns1[i].append(v.strip())

    # Combine two lists (id1,id2) into a list of tuples: previous transfers
    pay_network = zip(columns1[1], columns1[2])
    
    """ Initial payment network """
    pay_graph = Graph(pay_network)
    
    # Read filename2
    columns2 = defaultdict(list)
    
    with open(filename2, 'rU') as file2:
        reader2 = csv.reader(file2)
        reader2.next()
        for row in reader2:
            for (i,v) in enumerate(row):
                columns2[i].append(v.strip())
    
    # A list of tuples: new transfers
    new_transfer = zip(columns2[1], columns2[2])

    # 3 lists recording new transfer status, respectively relating to feature 1, 2, 3
    new_tranveri_fea1 = []
    new_tranveri_fea2 = []
    new_tranveri_fea3 = []

    for tuple in new_transfer:
        
        # Implement Feature 1:
        paypath_fea1 = pay_graph.find_feature1_path(tuple[0], tuple[1])
        if paypath_fea1:
            new_tranveri_fea1.append('trusted')
        else:
            new_tranveri_fea1.append('unverified')
        
        # Implement Feature 2:
        paypath_fea2 = pay_graph.find_feature2_path(tuple[0], tuple[1])
        if paypath_fea2:
            new_tranveri_fea2.append('trusted')
        else:
            new_tranveri_fea2.append('unverified')
        
        # Implement Feature 3:
        paypath_fea3 = pay_graph.find_feature3_path(tuple[0], tuple[1])
        if paypath_fea3:
            new_tranveri_fea3.append('trusted')
        else:
            new_tranveri_fea3.append('unverified')
        
        # Update 'pay_graph' with new incoming transfer
        pay_graph.add(tuple[0], tuple[1])

    # Write status of new transfers to 3 .txt files
    # feature 1 -> output1.txt, feature 2 -> output2.txt, feature 3 -> output3.txt
    with open(os.path.join(os.getcwd(), 'paymo_output/output1.txt'), 'w') as outfile1:
        for string in new_tranveri_fea1:
            outfile1.write('%s\n' % string)
    
    with open(os.path.join(os.getcwd(), 'paymo_output/output2.txt'), 'w') as outfile2:
        for string in new_tranveri_fea2:
            outfile2.write('%s\n' % string)

    with open(os.path.join(os.getcwd(), 'paymo_output/output3.txt'), 'w') as outfile3:
        for string in new_tranveri_fea3:
            outfile3.write('%s\n' % string)
    return 
    
def main():
    if len(sys.argv) != 4:
        print 'usage: ./PaymentVerify_SG.py  --transferverify file1 file2'
        sys.exit(1)

    option = sys.argv[1]
    filename1 = sys.argv[2]
    filename2 = sys.argv[3]
    if option == '--transferverify':
        transfer_verify(filename1, filename2)
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
    main()