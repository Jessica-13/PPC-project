#!/usr/bin/env python3


#import used modules
import sys
import time
import multiprocessing


#create a multiprocessing Queue object for sending messages to an input process
queueToInputProcess = multiprocessing.Queue()

#create a multiprocessing Queue object for receiving messages from an input process
queueFromInputProcess = multiprocessing.Queue()

#define a function to run continuously in a seperate process that monitors the pygame event queue for keypress events
def inputProcessLoop(queueToInputProcess,queueFromInputProcess):
	import pygame
	pygame.init()
	done = False
	while not done:
		now = time.time()
		pygame.event.pump()
		for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				response = event.unicode
				response_time = now
				queueFromInputProcess.put([response,response_time])
		if not queueToInputProcess.empty():
			from_queue = queueToInputProcess.get()
			if from_queue == 'quit':
				done = True


#start up the input detector in a separate process
inputProcess = multiprocessing.Process(target=inputProcessLoop, args=(queueToInputProcess,queueFromInputProcess,))
inputProcess.start()


#create a multiprocessing Queue object for sending messages to an output process
queueToOutputProcess = multiprocessing.Queue()

#define a function to run continuously in a seperate process that monitors the output queue for messages and writes data as necessary
def outputProcessLoop(queueToOutputProcess):
	outfile = open('outfile.txt','w')
	done = False
	while not done:
		if not queueToOutputProcess.empty():
			from_queue = queueToOutputProcess.get()
			if from_queue == 'quit':
				outfile.close()
				done = True
			else:
				outfile.write(from_queue+'\n')


#start up the output process in a separate process
outputProcess = multiprocessing.Process(target=outputProcessLoop, args=(queueToOutputProcess,))
outputProcess.start()

if __name__ == "__main__":

	#initialize pygame
	import pygame
	pygame.init()
	
	#initialize a font
	defaultFontName = pygame.font.get_default_font()
	feedbackFont = pygame.font.Font(defaultFontName, 100)

	#start the diaplay loop
	done = False
	updateDisplay = False
	while not done:
		if not queueFromInputProcess.empty():
			from_queue = queueFromInputProcess.get()
			if from_queue[0]=='\x1b':
				queueToInputProcess.put('quit')
				queueToOutputProcess.put('quit')
				inputProcess.join()
				outputProcess.join()
				pygame.quit()
				sys.exit()
			elif from_queue[0]=='i':
				screen = pygame.display.set_mode((1366,768),pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
				# screen = pygame.display.set_mode((400,400))
				screen.fill((0,0,0))
				pygame.display.flip()				
			else:
				toDisplay = from_queue[0]
				updateDisplay = True
		if updateDisplay:
			updateDisplay = False
			thisRender = feedbackFont.render(toDisplay, True, (255,255,255))
			x = screen.get_width()/2-thisRender.get_width()/2
			y = screen.get_height()/2-thisRender.get_height()/2
			screen.fill((0,0,0))
			screen.blit(thisRender,(x,y))
			pygame.display.flip()
			flipLatency = str(time.time()-from_queue[1])
			queueToOutputProcess.put(flipLatency)




'''
import pygame
import numpy as np
import threading
import time

class Logic:
    # This will run in another thread
    def __init__(self, size, speed=2):
        # Private fields -> Only to be edited locally
        self._size = size
        self._direction = np.array([0, 1])  # [x, y] vector, underscored because we want this to be private
        self._speed = speed

        # Threaded fields -> Those accessible from other threads
        self.position = np.array(size) / 2
        self.input_list = []  # A list of commands to queue up for execution

        # A lock ensures that nothing else can edit the variable while we're changing it
        self.lock = threading.Lock()

    def _loop(self):
        time.sleep(0.5)  # Wait a bit to let things load
        # We're just going to kill this thread with the main one so it's fine to just loop forever
        while True:
            # Check for commands
            time.sleep(0.01)  # Limit the logic loop running to every 10ms

            if len(self.input_list) > 0:

                with self.lock:  # The lock is released when we're done
                    # If there is a command we pop it off the list
                    key = self.input_list.pop(0).key

                if key == pygame.K_w:
                    self._direction = np.array([0, -1])
                elif key == pygame.K_a:
                    self._direction = np.array([-1, 0])
                elif key == pygame.K_s:
                    self._direction = np.array([0, 1])
                elif key == pygame.K_d:
                    self._direction = np.array([1, 0])

            with self.lock:  # Again we call the lock because we're editing
                self.position += self._direction * self._speed

            if self.position[0] < 0 \
                    or self.position[0] > self._size[0] \
                    or self.position[1] < 0 \
                    or self.position[1] > self._size[1]:
                break  # Stop updating

    def start_loop(self):
        # We spawn a new thread using our _loop method, the loop has no additional arguments,
        # We call daemon=True so that the thread dies when main dies
        threading.Thread(target=self._loop,
                         args=(),
                         daemon=True).start()


class Game:
    # This will run in the main thread and read data from the Logic
    def __init__(self, size, speed=2):
        self.size = size
        pygame.init()
        self.window = pygame.display.set_mode(size)
        self.logic = Logic(np.array(size), speed)
        self.running = True

    def start(self):
        pygame.display.update()
        self.logic.start_loop()

        # any calls made to the other thread should be read only
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # Here we call the lock because we're updating the input list
                    with self.logic.lock:
                        self.logic.input_list.append(event)

            # Another lock call to access the position
            with self.logic.lock:
                self.window.fill((0, 0, 0))
                pygame.draw.circle(self.window, (0, 0, 255), self.logic.position, 10)
                pygame.display.update()

        pygame.time.wait(10)
        pygame.quit()
        quit()


if __name__ == '__main__':
    game = Game([800, 600])
    game.start()'''








'''import pygame
import numpy as np

# Initialise parameters
#######################
size = np.array([800, 600])
position = size / 2
direction = np.array([0, 1])  # [x, y] vector
speed = 2
running = True

pygame.init()
window = pygame.display.set_mode(size)
pygame.display.update()

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                direction = np.array([0, -1])
            elif event.key == pygame.K_a:
                direction = np.array([-1, 0])
            elif event.key == pygame.K_s:
                direction = np.array([0, 1])
            elif event.key == pygame.K_d:
                direction = np.array([1, 0])

    position += direction * speed

    if position[0] < 0 or position[0] > size[0] or position[1] < 0 or position[1] > size[1]:
        running = False

    pygame.time.wait(10)  # Limit the speed of the loop

    window.fill((0, 0, 0))
    pygame.draw.circle(window, (0, 0, 255), position, 10)
    pygame.display.update()

pygame.quit()
quit()'''