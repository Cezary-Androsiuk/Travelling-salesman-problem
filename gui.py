import pygame
import threading
from time import sleep
import time
import queue

GUI_DEBUG = False

def startFunction(outputQueue, data, dataHandler):
    try:
        # compute path - k
        start = time.time()
        pathData, totalDistance = dataHandler(data)
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
        


def debugStartFunction(outputQueue, data, dataHandler):
    print(__name__ + " starting")
    sleep(2)
    print(__name__ + " ended")
    
    outputQueue.put({
        "correctlyFinished": False
    })

def gui(data, dataHandler):
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('lato', 45)
    windowSize = (700, 700)
    screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
    # screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE + pygame.NOFRAME)
    pygame.display.set_caption("Traveling Salesman Problem")
    clock = pygame.time.Clock()
    
    outputQueue = queue.Queue()

    computingFunction = debugStartFunction if GUI_DEBUG else startFunction
    taskThread = threading.Thread(target=computingFunction, args=(outputQueue, data, dataHandler))
    taskThread.start()

    # color stuff
    backgroundColor = (30, 30, 30)
    textColor =  (230, 230, 230)
    circleColor = (230, 40, 40)

    rawBackgroundImage = pygame.image.load("./country_maps/Poland-Map3.png")
    backgroundImage = pygame.transform.scale(rawBackgroundImage, windowSize)

    computingFunctionOutput = None

    running = True
    while running:
        # handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
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

        for city in data:
            x = (city["x"]/2000) * windowSize[0]
            y = (city["y"]/2000) * windowSize[1]
            pygame.draw.circle(screen, circleColor, (x, y), 4)


        if not outputQueue.empty():
            computingFunctionOutput = outputQueue.get()

        if computingFunctionOutput == None:
            textObj = font.render("Loading...", True, textColor)
        else:
            if computingFunctionOutput["correctlyFinished"]:
                textObj = font.render("Loaded!", True, textColor)
            else:
                textObj = font.render("Failed!", True, textColor)
            # print(1)
            # print(computingFunctionOutput)
            
            # add paths stuff here

        textObjRect = textObj.get_rect(center=(windowSize[0]/2, windowSize[1]/2))
        screen.blit(textObj, textObjRect)

        pygame.display.flip()
        clock.tick(20) # limit fps to 20

    pygame.quit()
