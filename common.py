import os
import sys
import json

import pygame
import pygame.gfxdraw
from pygame.color import THECOLORS

#import pymunk
#from pymunk.vec2d import Vec2d
#import pymunk.pygame_util


LEFTBUTTON = 1
CENTERBUTTON = 2
RIGHTBUTTON = 3

WAIT = 1
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
TICK = 50
HEADER = 50
MARGIN = 10

BACKGROUND_IMAGE = "background.png"

def fmt(n):
    if type(n) in (long, int):
        return "{:1,d}".format(n)
    elif type(n) is float:
        return "{:1,.1f}".format(n)
    else:
        return n

