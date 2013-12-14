try:
    import android
except ImportError:
    android = None

import os
import sys
import json

import pygame
pygame.init()
import pygame.gfxdraw
from pygame.color import THECOLORS

#import pymunk
#from pymunk.vec2d import Vec2d
#import pymunk.pygame_util

GAMEDIR = os.path.dirname(os.path.abspath(sys.argv[0]))


LEFTBUTTON = 1
CENTERBUTTON = 2
RIGHTBUTTON = 3

WAIT = 1
if not android:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
else:
# HTC Vivid -- 960, 540
# Nexus 7 (2012) -- 1280, 800
    SCREEN_WIDTH = 960
    SCREEN_HEIGHT = 540
if not android:
    if os.environ.get("USE_WINDOW"):
        DISPLAY_FLAGS = 0
        DISPLAY_FLAGS = pygame.DOUBLEBUF
    else:
        DISPLAY_FLAGS = pygame.FULLSCREEN|pygame.DOUBLEBUF
else:
    DISPLAY_FLAGS = 0
TICK = 50
HEADER = 50
MARGIN = 10


IMAGESET_KEY = os.environ.get("IMAGESET", "b").lower()
IMAGE_DIR = "imageset-%s" % (IMAGESET_KEY,)
BACKGROUND_IMAGE = os.path.join(IMAGE_DIR, "background.png")
GOLDEN_AVAILABLE_IMAGE = os.path.join(IMAGE_DIR, "golden-available.png")
GOLDEN_ACTIVE_IMAGE = os.path.join(IMAGE_DIR, "golden-active.png")
DONUT_IMAGE = os.path.join(IMAGE_DIR, "donut.png")
DONUT_CLICKED_IMAGE = os.path.join(IMAGE_DIR, "donut-clicked.png")
UPGRADE_STATE1_IMAGE = os.path.join(IMAGE_DIR, "placeholder1.png")
UPGRADE_STATE2_IMAGE = os.path.join(IMAGE_DIR, "placeholder2.png")
UPGRADE_STATE3_IMAGE = os.path.join(IMAGE_DIR, "placeholder3.png")
UPGRADE_STATE4_IMAGE = os.path.join(IMAGE_DIR, "placeholder4.png")
BUILDING1_IMAGE = os.path.join(IMAGE_DIR, "build1.png")
BUILDING2_IMAGE = os.path.join(IMAGE_DIR, "build2.png")

if IMAGESET_KEY == "a":
    TEXT_COLOR = (255, 255, 255, 255)
    TEXT_BACKGROUND = (25, 25, 25, 0)
    TEXT_ANTIALIAS = False
elif IMAGESET_KEY == "b":
    TEXT_COLOR = (255, 255, 255, 255)
    TEXT_BACKGROUND = (25, 25, 25, 20)
    TEXT_ANTIALIAS = False
else:
    TEXT_COLOR = (255, 255, 255, 255)
    TEXT_BACKGROUND = (25, 25, 25, 20)
    TEXT_ANTIALIAS = False


def fmt(n):
    if type(n) not in (long, int, float):
        return n
    if type(n) in (long, int):
        s = "{:1,d}".format(n)
    elif type(n) is float:
        s = "{:1,.1f}".format(n)
    parts = s.split(",")
    if len(parts) <= 3:
        return s
    if len(parts) == 4:
        return "%s thousand" % (",".join(parts[:3]))
    elif len(parts) == 5:
        return "%s million" % (",".join(parts[:3]))
    elif len(parts) == 6:
        return "%s billion" % (",".join(parts[:3]))
    elif len(parts) == 7:
        return "%s quadrillion" % (",".join(parts[:3]))
    elif len(parts) == 8:
        return "%s quintillion" % (",".join(parts[:3]))
    elif len(parts) == 9:
        return "%s sextillion" % (",".join(parts[:3]))
    elif len(parts) == 10:
        return "%s septillion" % (",".join(parts[:3]))
    elif len(parts) == 11:
        return "%s octillion" % (",".join(parts[:3]))
    elif len(parts) == 12:
        return "%s nonillion" % (",".join(parts[:3]))
    else:
        return s

    """
    6 aaa,bbb,ccc,ddd,eee,fff.234
    5 aaa,bbb,ccc,ddd,eee.234
    4 aaa,bbb,ccc,ddd.234   
    3 aaa,bbb,ccc.234
    2 aaa,bbb.234
    1 aaa.234
    """

