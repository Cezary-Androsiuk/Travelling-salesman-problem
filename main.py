from functions import readData, trimData, computePaths
from gui import gui

if __name__ == '__main__':
    cities = readData("city.data.txt")
    print(cities)

    # limit data by city or quantity - p
    cities = trimData(cities)

    gui(data=cities, dataHandler=computePaths)
