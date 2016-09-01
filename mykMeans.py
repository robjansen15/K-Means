from cmath import sqrt
import csv
import warnings
import random as rand
import numpy as numpy_
import sys
from datetime import datetime

#input data points
def readFile(fileName):
    with open(fileName,"rb") as f:
        reader = csv.reader(f)
        Data = list(reader)
    return numpy_.array(Data, dtype=numpy_.float64)

def readCentroidFile(fileName):
    with open(fileName,"rb") as f:
        reader = csv.reader(f)
        Data = list(reader)
    return numpy_.array(Data, int)

def getDistances(points,cent):
    data = []
    for x in points:
        for y in cent:
            value = sqrt(sum((x-y)**2))
            data.append(value)
    dist = numpy_.reshape(data, (len(points),len(cent)))
    return dist

#link centroid to closest centroid
def linkPointsToMin(distances, cluster_val):
    count = 0
    for x in distances:
        index = numpy_.argmin(x)
        cluster_val[count] = int(index)
        count=count+1
    return cluster_val

#update centroids based on new centroid - point mean
def updateCentroids(points, cluster_val):
    updatedCent = numpy_.zeros((kVal, dim), dtype=numpy_.float64)
    itt = 0
    while itt < kVal:
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                updatedCent[itt] = numpy_.mean(points[cluster_val == itt], axis=0)
            except RuntimeWarning:
                #error handling
                updatedCent = resetCentroids()
                break;
        itt = itt + 1
    return updatedCent

#update epsilon
def getEpsilon(old_cent, cent):
    eps = 0.0
    for col in range(0, dim):
        for row in range(0, kVal):
            eps += ((cent[row, col] - old_cent[row, col])**2)
    eps = sqrt(eps).real
    return eps

#re-initialize
def resetCentroids():
    xcent = numpy_.zeros((kVal, dim), dtype=numpy_.float64)
    for n in range(0, kVal):
        xcent[n, :] = points[rand.randint(0, items-1), :]
    return xcent

#overloaded for input from text file
def setCentroids(input_):
    xcent = numpy_.zeros((kVal, dim), dtype=numpy_.float64)
    for a in range(0, kVal):
        xcent[a, :] = points[input_[a], :]
    return xcent

#get the purity of the iris.txt
def getPurity():
    n_total = 0.
    pur = 0.
    A = numpy_.size((3,3))

    for o in range(0,items) :
        loc = int(o/50)
        A[loc,cluster_val[o]] = A[loc,cluster_val[o]] + 1

    for y in range (0,kVal) :
        max = numpy_.max(A,axis=1)
        n_total += max[y]

    pur = n_total / items
    return pur

#start main
c_kVal = 3
count = 0
epsilon = 1.0
centroid_file = ""
points_file = "datafile.txt"
rand.seed(datetime.now())

if len(sys.argv) == 3 :
    points_file = sys.argv[1]
    c_kVal = sys.argv[2]
elif len(sys.argv) == 4 :
    centroid_file = sys.argv[3]
else :
    print("I am not sure if you typed in the correct arguments...")

print
print
print "**************************************************"
print "****** Please check your arguments carefully *****"
print "**************************************************"

points = readFile(points_file)
items = len(points)
c_dim = len(points.sum(axis=0))
kVal = int(c_kVal)
dim = int(c_dim)
cent = numpy_.zeros(shape=(kVal, dim), dtype=numpy_.float64)

cluster_val = numpy_.zeros(items, dtype=int)

#initial clusters
if (centroid_file != "") :
    centroid_input = readCentroidFile(centroid_file)
    cent = setCentroids(centroid_input)
else :
    cent = resetCentroids()


#loop
while (epsilon > 0.001) :
    distance = getDistances(points,cent)
    cluster_val = linkPointsToMin(distance,cluster_val)
    old_cent = cent
    cent = updateCentroids(points,cluster_val)
    epsilon = getEpsilon(old_cent, cent)
    count = count + 1

SSE = 0
counter = 0
point_counter = 0
#sum of squared
for x in cent:
    for y in points:
        if counter == cluster_val[point_counter] :
            SSE += sqrt(sum((y-x)**2))
        point_counter = point_counter + 1
    point_counter = 0
    counter = counter + 1


#datt display
print
print
print "****************** Display Begin ******************"
print "Number of points: ", items
print "Dimension: ", dim
print "K-Value: ", kVal
print "Number of itterations: ", count
print "SSE score: ", SSE.real
print "Final cluster assigment of all the points: "
print (cluster_val)
print "Size of each cluster: "
num = 0
for t in range(0,kVal):
    for v in range(0,items):
        if cluster_val[v] == t:
            num = num + 1
    print "Centroid:", t, " - Number of points: ", num
    num = 0

print
print "************  CENTROIDS  ************"
print cent
print "************  END CENTROIDS  ************"

if(points_file == "iris.txt"):
    purity = getPurity()
    print "The purity is: ", purity

print
print "****************** Display End ******************"



