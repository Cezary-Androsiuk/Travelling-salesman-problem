

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
                    population=values[3]
                ))
                i+=1
    except Exception as e:
        print(f"Cannot open {citiesFilePath}: {e}")

    return cities

def trimData(citiesIn):
    citiesOut = citiesIn


    return citiesOut

def computePaths(citiesIn):
    # magic stuff

    return []