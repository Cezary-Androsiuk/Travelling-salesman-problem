
from functions import readData, trimData, computePaths

if __name__ == '__main__':
    cities = readData("city.data.txt")
    print(cities)

    # limit data by city or quantity - p
    cities = trimData(cities)

    # display window with info - c 

    # compute path - k
    paths = computePaths(cities);

    # display summary - c

    