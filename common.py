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
if os.environ.get("USE_WINDOW"):
    DISPLAY_FLAGS = 0
else:
    DISPLAY_FLAGS = pygame.FULLSCREEN
TICK = 50
HEADER = 50
MARGIN = 10



if os.environ.get("IMAGESET") == "1":
    TEXT_COLOR = (255, 255, 255)
    BACKGROUND_IMAGE = "a-background.png"
    GOLDEN_AVAILABLE_IMAGE = "a-golden-available.png"
    GOLDEN_ACTIVE_IMAGE = "a-golden-active.png"
    DONUT_IMAGE = "a-donut.png"
    UPGRADE_STATE1_IMAGE = "a-placeholder1.png"
    UPGRADE_STATE2_IMAGE = "a-placeholder2.png"
    UPGRADE_STATE3_IMAGE = "a-placeholder3.png"
    UPGRADE_STATE4_IMAGE = "a-placeholder4.png"
else:
    TEXT_COLOR = (255, 255, 255)
    BACKGROUND_IMAGE = "background.png"
    GOLDEN_AVAILABLE_IMAGE = "golden-available.png"
    GOLDEN_ACTIVE_IMAGE = "golden-active.png"
    DONUT_IMAGE = "donut.png"
    UPGRADE_STATE1_IMAGE = "placeholder1.png"
    UPGRADE_STATE2_IMAGE = "placeholder2.png"
    UPGRADE_STATE3_IMAGE = "placeholder3.png"
    UPGRADE_STATE4_IMAGE = "placeholder4.png"


def fmt(n):
    if type(n) in (long, int):
        return "{:1,d}".format(n)
    elif type(n) is float:
        return "{:1,.1f}".format(n)
    else:
        return n

