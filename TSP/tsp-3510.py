import sys
import time
import random
import math
from CityDistance import *

def computeDistance(path, distance):
    cost = 0
    for i in range(1, len(path)):
        cost += distance.get(path[i], path[i-1])
    cost += distance.get(path[0], path[-1])
    return cost

def computeCost(path,cost, distance):
    radius = random.random()
    if radius <= 0 or radius > 0.3:
        path1 = random.randint(0, len(path) - 1)
        path2 = (path1 + 1) % len(path)

        tempCost = cost

        tempCost -= distance.get(path[(path1 -1)%len(path)], path[path1])
        tempCost += distance.get(path[(path1 -1)%len(path)], path[path2])
        tempCost -= distance.get(path[path2], path[(path2 + 1)%len(path)])
        tempCost += distance.get(path[path1], path[(path2 + 1)%len(path)])
        return 2, path1, tempCost
    else:
        path1 = random.randint(0, len(path) - 1)
        path2 = random.randint(0, len(path) - 1)
        tempCost = cost
        if path1 != path2 and (path1 + 1)%len(path) != path2 and (path2 + 1)%len(path) != path1:
            tempCost -= distance.get(path[(path1 -1)%len(path)], path[path1])
            tempCost += distance.get(path[(path1 -1)%len(path)], path[path2])
            tempCost -= distance.get(path[path2], path[(path2 + 1)%len(path)])
            tempCost += distance.get(path[path1], path[(path2 + 1)%len(path)])
            return 1, path1, path2, tempCost
        return 1, 0 , 0 , tempCost

_, input_file, output_file, time_limit = sys.argv

#Starting time
inil_time = time.time()

#Ending time
max_time = inil_time + float(time_limit) - 0.015

places = [] #Places in the input files
coodinates = [] # Coordinates on the places
Result = {"path": None , "cost" : float("inf")}

#Result = [], float("inf")
#Reading the files and putting the city in a x,y coordinates
read_file = open(input_file, "r")
for city in read_file:
    num_city, x, y = city.split()
    x = float(x)
    y = float(y)
    num_city = int(num_city)
    places.append(num_city)
    coodinates.append((num_city, (x, y)))
read_file.close()

xy_distance = CityDistance() # Distance between 2 cities
#Calculating the distance from city a to city b
for x in range(0, len(coodinates) - 1):
    for y in range(x + 1, len(coodinates)):
        xy_distance.append(coodinates[x], coodinates[y])

#Algorithm
if len(places) is 0:
    Result["path"] = []
    Result["cost"] = 0

if len(places) is 1:
    Result["path"] = places
    Result["cost"] = 0

if len(places) is 2:
    cost = computeDistance(places, xy_distance)
    Result["path"] = places
    Result["cost"] = computeDistance(places, xy_distance)
    # Result = places,

#Generating path // places, xy_distance
temp_path = None

start = places[0]
temp_path = [start]
not_visited = set(places)
not_visited.remove(start)

while not_visited:
    min_distance = float("inf")
    min_path = None
    for i in not_visited:
        temp_distance = xy_distance.get(temp_path[-1], i)
        if temp_distance < min_distance:
            min_distance = temp_distance
            min_path = i
    temp_path.append(min_path)
    not_visited.remove(min_path)

temp_cost = computeDistance(temp_path, xy_distance)

start_time = time.time()
end_time = max_time - start_time + 0.05
avg_time = 0

while True:
    check_time = time.time()
    if check_time > max_time:
        break

    if temp_cost < Result["cost"]:
        Result["path"] = temp_path
        Result["cost"] = temp_cost
        # Result = temp_path, temp_cost
    #try a neighbor
    neighbor_path = computeCost(temp_path, temp_cost, xy_distance)
    if neighbor_path[0] is 1:
        x = neighbor_path[1]
        y = neighbor_path[2]
        new_cost = neighbor_path[3]
    else:
        x = neighbor_path[1]
        new_cost = neighbor_path[2]
    curr_time = end_time - (check_time - start_time)
    avg_time = (abs(temp_cost-new_cost) + avg_time * 1000) / 1001

#Def Chance
    new_temp_time = curr_time / end_time
    probability = 0
    if new_cost <= temp_cost:
        probability = 1
    try:
        probability = math.exp(-8 * (new_cost - temp_cost)/(new_temp_time * avg_time))
    except:
        probability = 0

    if random.random() < probability:
        if neighbor_path[0] is not 1:
            z = (x + 1)%len(temp_path)
            temp_place = temp_path[x]
            temp_path[x] = temp_path[z]
            temp_path[z] = temp_place
        if neighbor_path[0] is 1:
            if x is not y and (x + 1) % len(temp_path) is not y and (y+1)%len(temp_path) is not x:
                x_place = x
                y_place = y
                if x < y:
                    temp_max = (y-x+1) // 2
                else:
                    temp_max = (y + 1 + len(temp_path) - x) // 2
                for _ in range(temp_max):
                    temp_cont_path = temp_path[x_place]
                    temp_path[x_place] = temp_path[y_place]
                    temp_path[y_place] = temp_cont_path
                    x_place = (x_place + 1)%len(temp_path)
                    y_place = (y_place - 1)%len(temp_path)
        temp_cost = new_cost

out_ = open(output_file, "w")
out_.write("%d\n" % Result["cost"])
if len(Result["path"]) > 0:
    s = ""
    for i in Result["path"]:
        s += str(i) + " "
        print ("%s" %s)
    s += str(Result["path"][0])
    print ("%s" % s)
    out_.write(s)
out_.close()