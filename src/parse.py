import dag
import object
import random


result1 = open('horseTest.out', "r")
result2 = open('fake.out', "r")
outputFile = open('output.out', "a")


#from list to output format
# for i in result:
#     print(i)
#     newText = []
#     for letter in str(i):
#         # print(letter)
#         if letter != '[' and letter != ',' and letter != ']' and letter != '.':
#             newText.append(letter)
#         if (letter == ']'):
#             newText.append(';')
#     # print(newText)
#     s = ''.join(newText)
#     result2.write("2" + ". " + s)
    # print(i)
    
# from output to list
def convertString2List(result):
    totalPath = []
    for line in result:
        path = []
        temp = [[s] for s in line.rstrip().split('; ')]
        for t in temp:
            path += [[int(s) for s in t[0].split(' ')]]
        totalPath += [path]
    return (totalPath)
# result2.write("2" + ". " + str(newText))

def compute_score(graph, list_of_path):
    """take in a graph and a pathes and compute the score
    under the assuption that the proposed soln is valid"""
    vertices = graph.vertices
    score = 0
    base = 0
    for v in list_of_path:
        base += vertices[v].value
    score += base * len(list_of_path)
    return score

def compute_score_full_assignment(graph, paths):
    """take in a graph and a full assignment lists of pathes and compute the total score of the given soln"""
    total = 0
    for path in paths:
        total += compute_score(graph, path)
    return total

def computeScoreOfPath(i, path1, path2):
    g = object.Graph("../inputs/all/"+str(i)+".in")
    path1Score = compute_score_full_assignment(graph, path1)
    path2Score = compute_score_full_assignment(graph, path2)
    if path1Score >= path2Score:
        return 1
    else:
        return 2


PATH1 = convertString2List(result1)
PATH2 = convertString2List(result2)

for i in range(0, 600)