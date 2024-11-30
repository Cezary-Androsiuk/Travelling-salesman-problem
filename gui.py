import pygame
import threading
from time import sleep
import time
import queue

GUI_DEBUG = False

def debugStartFunction(outputQueue, runtimeQueue, data, dataHandler):
    print(__name__ + " starting")
    sleep(2)
    print(__name__ + " ended")
    
    outputQueue.put({
        "correctlyFinished": False
    })

# distance between Białystok(1721, 615) and Szczecin(120, 524) in our data is 1603.5841106721
# distance between these cities in real world is 573165.1m, or 573.17 km
# then ratio are:
REALISTIC_DISTANCE_RATIO_M = 573165.1/1603.5841106721
REALISTIC_DISTANCE_RATIO_KM = 573.17/1603.5841106721


originalDataSize = (2000, 2000)
windowSize = (900, 900)


def startFunction(outputQueue, runtimeQueue, data, dataHandler):
    try:
        # compute path - k
        start = time.time()
        pathData, totalDistance = dataHandler(data, runtimeQueue)
        end = time.time()
        # console stuff
        print(pathData) #[points:[x1,y1,name1],[x2,y2,name2]..., distances: [distance1-2, distance2-3,...]
        # To access points use pathData["points"]
        print("\n\n\n")
        print(pathData["points"])
        # To access point distances use pathData["distances"]
        print("\n\n\n")
        print(pathData["distances"])
        print("\n\n\n")
        print(f"Total distance: {totalDistance}")
        print("\n\n\n")
        print(f"Start time: {start}")
        print(f"End time: {end}")

        print(f"Total time: {end-start} seconds.")
        outputQueue.put({
            "correctlyFinished": True,
            "pathData": pathData,
            "totalDistance": totalDistance
        })
    except:
        print("Computing path failed!")
        outputQueue.put({
            "correctlyFinished": False
        })

def normalizePoint(x: int, y: int):
    global originalDataSize, windowSize
    normalizedX = (x/originalDataSize[0]) * windowSize[0]
    normalizedY = (y/originalDataSize[1]) * windowSize[1]
    return (normalizedX, normalizedY)
    
def drawTracePath(screen: pygame.Surface, points: list, lineColor: tuple):
    pointsCount = len(points)
    for i in range(pointsCount-1):
        start_pos = normalizePoint(points[i][0], points[i][1])
        end_pos = normalizePoint(points[i+1][0], points[i+1][1])
        pygame.draw.line(screen, lineColor, start_pos, end_pos, width=1)

def gui(data, dataHandler):
    global originalDataSize, windowSize

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('lato', 45)
    screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
    # screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE + pygame.NOFRAME)
    pygame.display.set_caption("Traveling Salesman Problem")
    clock = pygame.time.Clock()
    
    outputQueue = queue.Queue()
    runtimeQueue = queue.Queue()

    computingFunction = debugStartFunction if GUI_DEBUG else startFunction
    taskThread = threading.Thread(target=computingFunction, args=(outputQueue, runtimeQueue, data, dataHandler))
    taskThread.start()

    # color stuff
    backgroundColor = (30, 30, 30)
    textColor =  (230, 230, 230)
    pointColor = (170, 40, 40)
    lineColor = (170, 170, 170)


    initialImageIndex = 3 # 1-5
    rawBackgroundImage = pygame.image.load("./country_maps/Poland-Map"+str(initialImageIndex)+".png")
    backgroundImage = pygame.transform.scale(rawBackgroundImage, windowSize)

    computingFunctionOutput = None
    runtimeFunctionOutput = None
    dataLoadedCorrectly = False
    dataLoadFailed = False

    running = True
    while running:
        # handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                numberPressed = None

                if event.key == pygame.K_ESCAPE: running = False
                elif event.key == pygame.K_1: numberPressed = 1
                elif event.key == pygame.K_2: numberPressed = 2
                elif event.key == pygame.K_3: numberPressed = 3
                elif event.key == pygame.K_4: numberPressed = 4
                elif event.key == pygame.K_5: numberPressed = 5

                if numberPressed != None:
                    rawBackgroundImage = pygame.image.load("./country_maps/Poland-Map"+str(numberPressed)+".png")
                    backgroundImage = pygame.transform.scale(rawBackgroundImage, windowSize)

            elif event.type == pygame.VIDEORESIZE: # keep window size ratio 1:1
                oldSize = windowSize[0]
                newSize = oldSize

                if event.w != oldSize and event.h != oldSize:
                    newSize = min(event.w, event.h)
                elif event.w != oldSize:
                    newSize = event.w
                elif event.h != oldSize:
                    newSize = event.h

                windowSize = (newSize, newSize)
                screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
                backgroundImage = pygame.transform.scale(rawBackgroundImage, windowSize)


        screen.fill(backgroundColor)
        screen.blit(backgroundImage, (0,0))
        
        # draw cities
        for city in data:
            normalizedPoint = normalizePoint(city["x"], city["y"])
            pygame.draw.circle(screen, pointColor, normalizedPoint, 4)

        
        # react on computing finished
        if not outputQueue.empty(): # queue changes after function finish computing
            computingFunctionOutput = outputQueue.get()
            if computingFunctionOutput["correctlyFinished"]:
                dataLoadedCorrectly = True
            else:
                dataLoadFailed = True

        if dataLoadedCorrectly:
            # textObj = font.render("Loaded!", True, textColor)
            textObj = None

            # draw paths between cities
            points = computingFunctionOutput["pathData"]["points"]
            drawTracePath(screen, points, lineColor)
        elif dataLoadFailed:
            textObj = font.render("Computing Failed!", True, textColor)
        else:
            textObj = font.render("Computing...", True, textColor)

            # if any new data shows up, then draw it
            if not runtimeQueue.empty(): # read the newest
                runtimeFunctionOutput = runtimeQueue.get()
                
                # remove oldest if exists
                while not runtimeQueue.empty():
                    runtimeQueue.get_nowait();

            # draw the newest element
            drawTracePath(screen, runtimeFunctionOutput, lineColor)

        
        # draw info text if exist
        if textObj != None:
            textObjRect = textObj.get_rect(center=(windowSize[0]/2, windowSize[1]/2))
            pygame.draw.rect(screen, (0,0,0), textObjRect)
            screen.blit(textObj, textObjRect)

        pygame.display.flip() # update window with new data

        if not dataLoadedCorrectly:
            clock.tick(30) # limit fps to 10 frames per second, to not disturb computing algorithm

    pygame.quit()
