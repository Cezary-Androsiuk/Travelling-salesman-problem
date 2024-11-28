import pygame
import threading
from time import sleep
import queue


def startFunction(outputQueue, data, dataHandler):
    
    # compute path - k
    pathData, totalDistance = dataHandler(data)

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

    outputQueue.put(pathData)

def gui(data, dataHandler):
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('lato', 35)
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Traveling Salesman Problem")
    
    outputQueue = queue.Queue()

    taskThread = threading.Thread(target=startFunction, args=(outputQueue, data, dataHandler))
    taskThread.start()

    # color stuff
    backgroundColor = (30, 30, 30)
    textColor =  (230, 230, 230)

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

        if outputQueue.empty():
            textObj = font.render("Loading...", True, textColor)
        else:
            textObj = font.render("Loaded!", True, textColor)
            
            # add paths stuff here

        textObjRect = textObj.get_rect(center=(1280/2, 720/2))
        screen.blit(textObj, textObjRect)

        pygame.display.flip()

    pygame.quit()
