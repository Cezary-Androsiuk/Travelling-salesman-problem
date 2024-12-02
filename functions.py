import numpy as np
from aco import ACO
import random
import queue
import os

def randomizeInputData(cities):
    shuffledCities = cities[:]
    random.shuffle(shuffledCities)
    return shuffledCities

def readData(citiesFilePath):
    cities = []
    try:
        with open(citiesFilePath, 'r', encoding='utf-8') as citiesFile:
            # print("oppened")
            i = 0
            for rawCity in citiesFile:
                # print(f"index {i}")
                values = rawCity.strip().split(' ')

                cityName = values[2].replace('_', ' ')

                cities.append(dict(
                    index=i, 
                    x=int(values[0]), y=int(values[1]), 
                    cityName=cityName,
                    population=int(values[3])
                ))
                i+=1
    except Exception as e:
        print(f"Cannot open {citiesFilePath}: {e}")

    return randomizeInputData(cities)

def trimData(citiesIn):
    citiesOut = citiesIn
    selection_file = "selection.txt"

    if os.path.exists(selection_file):
        with open(selection_file, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]

        if lines:
            if len(lines) == 1 and lines[0].isdigit():
                num_cities = int(lines[0])
                if num_cities >= len(citiesIn):
                    citiesOut = citiesIn
                else:
                    citiesOut = random.sample(citiesIn, num_cities)
            else:
                selected_names = {line for line in lines}
                citiesOut = [city for city in citiesIn if city['cityName'] in selected_names]

    print(citiesOut)
    return citiesOut

# Get the necessary info about the point for further computing (x, y, name).
def getPoints(citiesIn):
    points = []
    for i in range(len(citiesIn)):
        point = [citiesIn[i]['x'], citiesIn[i]['y'], citiesIn[i]['cityName']]
        points.append(point)
    return points

# Calculate the distance matrix used by the algorithm.
def getDistanceMatrix(points):
    n = len(points)
    distanceMatrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distanceMatrix[i,j] = np.sqrt((points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2)
    np.fill_diagonal(distanceMatrix, np.inf)
    return distanceMatrix


def computePaths(citiesIn, guiQueue: queue.Queue):
    points = getPoints(citiesIn)  # Get [x, y, cityName]
    distanceMatrix = getDistanceMatrix(points)

    # Run ACO algorithm
    aco = ACO(distanceMatrix, points, 10, 5, 100, 0.95, 1, 1)  # Adjusted parameters
    shortest = aco.run(guiQueue)

    shortest_indices = shortest[0]  # Indices of cities in the shortest path
    shortest_distance = shortest[1]  # Total distance of the shortest path

    # Prepare data structure to hold path and distances
    path_data = {"points": [], "distances": []}

    # Populate points and distances
    for (a, b) in shortest_indices:
        # Add full point info: (x, y, cityName)
        if points[a] not in path_data["points"]:
            path_data["points"].append(points[a])  # Full point info for plotting
        path_data["points"].append(points[b])

        # Add distance
        distance = distanceMatrix[a, b]
        path_data["distances"].append(float(distance))

    # Print results
    print("Path points (coordinates and names):", path_data["points"])
    print("Distances between points:", path_data["distances"])
    print(f"Total distance: {shortest_distance:.2f}")

    return path_data, shortest_distance



