
from functions import readData, trimData, computePaths

if __name__ == '__main__':
    cities = readData("city.data.txt")
    print(cities)

    # limit data by city or quantity - p
    cities = trimData(cities)

    # display window with info - c 

    # compute path - k
    pathData, totalDistance = computePaths(cities)

    print(pathData) #[points:[x1,y1,name1],[x2,y2,name2]..., distances: [distance1-2, distance2-3,...]
    # To access points use pathData["points"]
    print(pathData["points"])
    # To access point distances use pathData["distances"]
    print(pathData["distances"])
    print(totalDistance)



    # display summary - c

    