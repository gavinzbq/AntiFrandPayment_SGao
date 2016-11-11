#!/usr/bin/python -tt

"""
Import input csv files, store values of each header in columns with numerical index:
time:0, id1:1, id2:2, amount:3, message:4
Combine column[1] and [2] as a list of tuples: [('id1', 'id2'), then generate payment 
network graph. The graph will be updated with incoming transfers (each line in 
filename2).

Use the exisiting payment network to verify each new transfer, based on graph theory.
"""  

import csv
import os

import payment_graph

def transfer_verify(filename1, filename2):
    
    from collections import defaultdict

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
    pay_graph = payment_graph.Graph(pay_network)
    
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