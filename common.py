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

from fmt import fmt

#import pymunk
#from pymunk.vec2d import Vec2d
#import pymunk.pygame_util


DEBUG = int(os.environ.get("DEBUG", 0))
MODE = int(os.environ.get("MODE", 2))

GAMEDIR = os.path.dirname(os.path.abspath(sys.argv[0]))


VERSION = "0.0.6"


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
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
if not android:
    if os.environ.get("USE_WINDOW"):
        DISPLAY_FLAGS = 0
        DISPLAY_FLAGS = pygame.DOUBLEBUF
    else:
        DISPLAY_FLAGS = pygame.FULLSCREEN|pygame.DOUBLEBUF
else:
    DISPLAY_FLAGS = 0
TICK = 12
HEADER = 50
MARGIN = 10


IMAGESET_KEY = os.environ.get("IMAGESET", "b").lower()
IMAGE_DIR = "imageset-%s" % (IMAGESET_KEY,)
BACKGROUND_IMAGE = os.path.join(IMAGE_DIR, "darkblue-background.png")
ROCKWELL_IMAGE = os.path.join(IMAGE_DIR, "rockwell.png")
GOLDEN_AVAILABLE_IMAGE = os.path.join(IMAGE_DIR, "golden-available.png")
GOLDEN_ACTIVE_IMAGE = os.path.join(IMAGE_DIR, "golden-active.png")
DONUT_IMAGE = os.path.join(IMAGE_DIR, "donut.png")
DONUT_CLICKED_IMAGE = os.path.join(IMAGE_DIR, "donut-clicked.png")
DONUT_RED_IMAGE = os.path.join(IMAGE_DIR, "donut-red.png")
DONUT_ORANGE_IMAGE = os.path.join(IMAGE_DIR, "donut-orange.png")
DONUT_YELLOW_IMAGE = os.path.join(IMAGE_DIR, "donut-yellow.png")
DONUT_GREEN_IMAGE = os.path.join(IMAGE_DIR, "donut-green.png")
DONUT_BLUE_IMAGE = os.path.join(IMAGE_DIR, "donut-blue.png")
BUILDING1_IMAGE = os.path.join(IMAGE_DIR, "build1.png")
BUILDING2_IMAGE = os.path.join(IMAGE_DIR, "build2.png") 
BUTTON_BACK_IMAGE = os.path.join(IMAGE_DIR, "button-back.png")         # 147x46
BUTTON_RESET_IMAGE = os.path.join(IMAGE_DIR, "button-reset.png")       # 147x46
BUTTON_CREDITS_IMAGE = os.path.join(IMAGE_DIR, "button-credits.png")   # 147x46
BUTTON_STATS_IMAGE = os.path.join(IMAGE_DIR, "button-stats.png")       # 147x46
BUTTON_PLAY_IMAGE = os.path.join(IMAGE_DIR, "button-play.png")         # 147x46
BUTTON_PROFILES_IMAGE = os.path.join(IMAGE_DIR, "button-profiles.png") # 147x46


if IMAGESET_KEY == "a":
    TEXT_COLOR = (255, 255, 255, 255)
    TEXT_BACKGROUND = (25, 25, 25, 0)
    TEXT_ANTIALIAS = False
elif IMAGESET_KEY == "b":
    TEXT_COLOR = (255, 255, 255, 255)
    TEXT_BACKGROUND = (25, 25, 25, 20)
    TEXT_COLOR = (255, 255, 255, 255)
    TEXT_COLOR = (33, 50, 64, 255)
    TEXT_COLOR = (128, 66, 0, 255)
    TEXT_COLOR = (0, 0, 0, 255)
    TEXT_COLOR = (255, 255, 255, 255)
    TEXT_BACKGROUND = (25, 25, 25, 20)
    TEXT_BACKGROUND = None
    TEXT_ANTIALIAS = True
else:
    TEXT_COLOR = (255, 255, 255, 255)
    TEXT_BACKGROUND = (25, 25, 25, 20)
    TEXT_ANTIALIAS = False


def make_text(font, text, antialias, color, bg_color):
    """
    returns a surface
    """
    return font.render(text, antialias, color)
    if bg_color is None:
        surface = font.render(text, antialias, color)
    else:
        surface = font.render(text, antialias, color, bg_color)
    return surface

