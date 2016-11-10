# Insight Data Engineering Coding Challenge

###Shanyun Gao

shanyun@g.clemson.edu


##Challenge Summary

Implement features to prevent fraudulent payment requests from untrusted users. 

###Feature 1
When anyone makes a payment to another user, they'll be notified if they've never made a transaction with that user before.


###Feature 2
Prevent payment transfers between two users when they are outside "2nd-degree friends network".

<img src="./images/friend-of-a-friend1.png" width="500">


###Feature 3
More generally, implement a feature to warn users only when they are outside the "4th-degree friends network".

<img src="./images/fourth-degree-friends2.png" width="600">


##Solution Description

The best way to represent the payment transfer network is using graph, and for graph, the simplest and most elegant data structure in Python is a dict of sets. Users are *vertices*, transfer actions are *edges* (undirected), therefore to verify a payment request between two users is equivalent to finding path between two vertices, with a maximum path length. For feature 1, path length over 2 is "unverified", feature 2 cannot exceed 3 ,and feature 3 needs to be less than or equal to 5.

The first part of this challenge is to build the initial payment network graph ,using data from `batch_payment.txt` in `paymo_input` directory. I implemented a Python graph class, with essential functionalities of graphs such as adding connections, adding connection between two nodes. The most important functionality is finding paths connecting two given nodes. The algorithm I chose is Depth First Search with depth limit: to find and return a path whose length is under the given maximum length (feature 1 is 2, feature 2 is 3, feature 3 is 5). The chosen algorithm is efficient and cache-friendly, therefore guarantees optimized performance. 


##Implementation

The program can be launched by running *run.sh* Bash script:

`./run.sh`

To manually run the program and print output files to `/paymo_output` directory:

`python ./src/PaymentVerify_SG --transferverify ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt`

	 
##Results

`batch_payment.txt` was used to generate the graph representing the initial payment network. 

File `NewTransfer.txt` is the first 20 lines from `stream_payment.txt`. By running command: 

`python ./src/PaymentVerify_SG --transferverify ./paymo_input/batch_payment.txt ./paymo_input/NewTransfer_payment.txt`

three output .txt files were generated in `/paymo_output` directory. The results are when implementing *feature 1*:

`unverified
trusted
trusted
trusted
trusted
unverified
trusted
unverified
trusted
trusted
unverified
unverified
unverified
trusted
unverified
unverified
unverified
unverified
trusted
`

*feature 2*:

`trusted
trusted
trusted
trusted
trusted
unverified
trusted
unverified
trusted
trusted
trusted
trusted
unverified
trusted
trusted
trusted
trusted
trusted
trusted
`

*feature 3*:

`trusted
trusted
trusted
trusted
trusted
trusted
trusted
trusted
trusted
trusted
trusted
trusted
unverified
trusted
trusted
trusted
trusted
trusted
trusted
`

It can be observed that there is an increase in *trusted* payment requests when expanding the feature to large social network.


##Dependency

* *Python 2.7.10*
