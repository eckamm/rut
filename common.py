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


IMAGESET_KEY = os.environ.get("IMAGESET", "a").lower()
BACKGROUND_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "background.png")
GOLDEN_AVAILABLE_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "golden-available.png")
GOLDEN_ACTIVE_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "golden-active.png")
DONUT_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "donut.png")
DONUT_CLICKED_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "donut-clicked.png")
UPGRADE_STATE1_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "placeholder1.png")
UPGRADE_STATE2_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "placeholder2.png")
UPGRADE_STATE3_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "placeholder3.png")
UPGRADE_STATE4_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "placeholder4.png")
BUILDING1_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "build1.png")
BUILDING2_IMAGE = os.path.join("imageset-%s" % (IMAGESET_KEY,), "build2.png")

if IMAGESET_KEY == "a":
    TEXT_COLOR = (255, 255, 255)
elif IMAGESET_KEY == "b":
    TEXT_COLOR = (255, 255, 255)
else:
    TEXT_COLOR = (255, 255, 255)


def fmt(n):
    if type(n) in (long, int):
        return "{:1,d}".format(n)
    elif type(n) is float:
        return "{:1,.1f}".format(n)
    else:
        return n

