# Author: Joseph Kuhn

#  triad_graphs.py takes data from a CSV file and determines how many triangles there are,
#  as well as how many different types of relationships exist.
#  This program identifies triads and calculates a lot of different data, including the expected
#  number of different relationships vs. the actual number.

# to run from terminal window:  
#      python3 triad_graphs.py
#  When asked to input a file name, enter the file name with the extension
# For example: epinions96.csv

import csv
import networkx

#setting up variables
numEdges = 0
numSelfLoops = 0
TotEdges = 0 # numEdges - numSelfLoops
numTrust = 0
numDistrust = 0
probabilityPos = 0 # num positive edges / totEdges
probabilityNeg = 0 # 1 - probabilityPos
numTriangles = 0
TTT = 0
TTD = 0
TDD = 0
DDD = 0

graph = networkx.Graph() # sets up a graph

f = input("Enter file name with extension: ") # takes in file name

with open(f, 'r') as openFile:
    readFile = csv.reader(openFile, delimiter = ',')
    for line in readFile: # runs through every line of the file
        numEdges = numEdges + 1
        if int(line[0]) == int(line[1]): # check for self-loops
            numSelfLoops = numSelfLoops + 1
            continue
        graph.add_edge(int(line[0]), int(line[1]), relation = int(line[2])) # add new edges
        if int(line[2]) == 1: # check if it's a trusted edge
            numTrust = numTrust + 1
        elif int(line[2]) == -1: # check if it's not a trusted edge
            numDistrust = numDistrust + 1

for edge in graph.edges:
    for node in graph.nodes:
        if graph.has_edge(edge[0], node) and graph.has_edge(edge[1], node): # go through nodes of each edge and see if there's a triad
            relat1 = graph[node][edge[0]]["relation"]
            relat2 = graph[node][edge[1]]["relation"]
            relat3 = graph[edge[0]][edge[1]]["relation"]
            counter = 0 # keep note of the relationships of each triad

            if relat1 == 1:
                counter = counter + 1
            if relat2 == 1:
                counter = counter + 1
            if relat3 == 1:
                counter = counter + 1
            if counter == 3:
                TTT = TTT + 1
            elif counter == 2:
                TTD = TTD + 1
            elif counter == 1:
                TDD = TDD + 1
            else:
                DDD = DDD + 1
            numTriangles = numTriangles + 1
            

numTriangles = int(numTriangles / 3)
TTT = int(TTT / 3)
TTD = int(TTD / 3)
TDD = int(TDD / 3)
DDD = int(DDD / 3)
totEdges = numEdges - numSelfLoops
probabilityPos = round(numTrust / totEdges, 2)
probabilityNeg = round(1 - probabilityPos, 2)
# probability of getting these different relationships
TTTprob = round(100 * probabilityPos * probabilityPos * probabilityPos, 1)
TTDprob = round(3 * 100 * probabilityPos * probabilityPos * probabilityNeg, 1)
TDDprob = round(3* 100 * probabilityPos * probabilityNeg * probabilityNeg, 1)
DDDprob = round(100 * probabilityNeg * probabilityNeg * probabilityNeg, 1)
# number of these relationships in the data
TTTnum = round(TTTprob / 100 * numTriangles, 1)
TTDnum = round(TTDprob / 100 * numTriangles, 1)
TDDnum = round(TDDprob / 100 * numTriangles, 1)
DDDnum = round(DDDprob / 100 * numTriangles, 1)

TTTprobAct = round(100 * TTT / numTriangles, 1)
TTDprobAct = round(100 * TTD / numTriangles, 1)
TDDprobAct = round(100 * TDD / numTriangles, 1)
DDDprobAct = round(100 * DDD / numTriangles, 1)

# print everything

print("Edges in network: " + str(numEdges))
print("Self-loops: " + str(numSelfLoops))
print("Total Edges (edges used - self-loops): " + str(totEdges))
print("Trust Edges: " + str(numTrust))
print("Distrust Edges: " + str(numDistrust))
print("Probability that an edge will be positive (p): " + str(probabilityPos))
print("Probability that an edge will be negative (1 - p): " + str(probabilityNeg))
print("Triangles: " + str(numTriangles))
print("Expected Distribution")
print("Type  Percent  Number")
print("TTT    " + str(TTTprob) + "      " + str(TTTnum))
print("TTD    " + str(TTDprob) + "      " + str(TTDnum))
print("TDD    " + str(TDDprob) + "      " + str(TDDnum))
print("DDD    " + str(DDDprob) + "      " + str(DDDnum))
print("Total  " + str(round(TTTprob + TTDprob + TDDprob + DDDprob, 1)) + "     " + str(round(TTTnum + TTDnum + TDDnum + DDDnum, 1)))
print("")
print("Actual Distribution")
print("Type  Percent  Number")
print("TTT    " + str(TTTprobAct) + "      " + str(TTT))
print("TTD    " + str(TTDprobAct) + "      " + str(TTD))
print("TDD    " + str(TDDprobAct) + "      " + str(TDD))
print("DDD     " + str(DDDprobAct) + "      " + str(DDD))
print("Total  " + str(round(TTTprobAct + TTDprobAct + TDDprobAct + DDDprobAct, 1)) + "     " + str(numTriangles))