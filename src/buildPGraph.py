#!/usr/bin/python -tt

"""
work on the Insight Data Engineering coding challenge in a different approach,
still use graph theory, breadth first search algorithm
"""

import time
import sys
import csv
from pythonds.graphs import Graph, Vertex
from pythonds.basic import Queue

def genUser(filename):
    with open(filename, 'rU') as file:
        reader = csv.reader(file)
        # skip header line
        reader.next()
        for row in reader:
            # check if that row has complete transfer information (time, id12, amouont)
            if len(row) >= 4:
                yield (row[1].strip(), row[2].strip()) 

def buildGraph(filename):
    payG = Graph()

    for users in genUser(filename):
        payG.addEdge(users[0], users[1])
        
    return payG

# implement BFS
def searchPath(payG, node1, node2, max_dist):
    node1.setDistance(0)
    node1.setPred(None)
    vertQueue = Queue()
    vertQueue.enqueue(node1)
    lenPath = 0

    while lenPath <= max_dist and vertQueue.size() > 0:
        currentVert = vertQueue.dequeue()
        for nbr in currentVert.getConnections():
            if (nbr.getColor() == 'white'):
                nbr.setColor('gray')
                nbr.setDistance(currentVert.getDistance() + 1)
                nbr.setPred(currentVert)
                vertQueue.enqueue(nbr)
        currentVert.setColor('black')
        lenPath = nbr.dist

    if node2.getColor() != 'white':
        return True
    else:
        return False

# Note that: max_dist = number of degree (friends network) - 1
def verifyNew(filename1, filename2, max_dist):

    payG = buildGraph(filename1) 

    for users in genUser(filename2):
        
        start = time.time()
        print searchPath(payG, payG.getVertex(users[0]), payG.getVertex(users[1]), max_dist)
        end = time.time()
        print (end - start)

        # update payment graph
        payG.addEdge(users[0], users[1])

def main():
    if len(sys.argv) != 4:
        print 'usage: ./buildPGraph.py verify file1 file2'
        sys.exit(1)

    option = sys.argv[1]
    filename1 = sys.argv[2]
    filename2 = sys.argv[3]
    if option == 'verify':
        verifyNew(filename1, filename2, 3)
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
    main()
