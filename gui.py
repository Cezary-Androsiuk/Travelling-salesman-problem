import pygame
import threading
from time import sleep
import time
import queue

GUI_DEBUG = False

def startFunction(outputQueue, data, dataHandler):
    
    outputData = {
        "correctlyFinished": False
    }

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
        outputData = {
            "correctlyFinished": True,
            "pathData": pathData,
            "totalDistance": totalDistance
        }
    except:
        print("Computing path failed!")

    outputQueue.put(outputData)

def debugStartFunction(outputQueue, data, dataHandler):
    print(__name__ + " starting")
    sleep(2)
    print(__name__ + " ended")
    outputQueue.put([])

def gui(data, dataHandler):
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('lato', 35)
    windowSize = (1280, 720)
    screen = pygame.display.set_mode(windowSize)
    pygame.display.set_caption("Traveling Salesman Problem")
    
    outputQueue = queue.Queue()

    computingFunction = debugStartFunction if GUI_DEBUG else startFunction
    taskThread = threading.Thread(target=computingFunction, args=(outputQueue, data, dataHandler))
    taskThread.start()

    # color stuff
    backgroundColor = (30, 30, 30)
    textColor =  (230, 230, 230)

    backgroundImage = pygame.image.load("./country_maps/Poland-Map3.png")
    backgroundImage = pygame.transform.scale(backgroundImage, windowSize)

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

        screen.fill(backgroundColor)
        


        if not outputQueue.empty():
            computingFunctionOutput = outputQueue.get()

        if computingFunctionOutput == None:
            textObj = font.render("Loading...", True, textColor)
        else:
            # print(1)
            textObj = font.render("Loaded!", True, textColor)
            # print(computingFunctionOutput)
            
            # add paths stuff here

        textObjRect = textObj.get_rect(center=(windowSize[0]/2, windowSize[1]/2))
        screen.blit(textObj, textObjRect)

        pygame.display.flip()

    pygame.quit()
