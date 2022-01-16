#!/usr/bin/env python3



import threading

class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            d = self.input_cbk(input()) #waits to get input + Return

showcounter = 0 #something to demonstrate the change

def my_callback(inp):
    #evaluate the keyboard input
    print('You Entered:', inp, ' Counter is at:', showcounter)

#start the Keyboard thread
kthread = KeyboardThread(my_callback)

while True:
    #the normal program executes without blocking. here just counting up
    showcounter += 1








'''
import sys
import select
import tty
import termios

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

old_settings = termios.tcgetattr(sys.stdin)
try:
    tty.setcbreak(sys.stdin.fileno())

    i = 0
    while 1:
        print(i)
        i += 1

        if isData():
            c = sys.stdin.read(1)
            if c == '\x1b':         # x1b is ESC
                break

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
'''




'''
import pygame
from pygame.locals import *

def display(str):
    text = font.render(str, True, (255, 255, 255), (159, 182, 205))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery

    screen.blit(text, textRect)
    pygame.display.update()

pygame.init()
screen = pygame.display.set_mode( (640,480) )
pygame.display.set_caption('Python numbers')
screen.fill((159, 182, 205))

font = pygame.font.Font(None, 17)

num = 0
done = False
while not done:
    display( str(num) )
    num += 1

    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        done = True
'''