import os
import sys

import pygame
import pygame.gfxdraw
from pygame.color import THECOLORS

#import pymunk
#from pymunk.vec2d import Vec2d
#import pymunk.pygame_util


import ex1


LEFTBUTTON = 1
CENTERBUTTON = 2
RIGHTBUTTON = 3

WAIT = 1
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
TICK = 50
HEADER = 50
MARGIN = 10


class XWidget:
    def __init__(self):
        self.cps = 0
        self.cookies = 0
        self._font = pygame.font.SysFont(None, 30)

    def draw(self, surface):
        cps_render = self._font.render("CPS: %d" % self.cps, True, (255,255,255))
        cps_box = cps_render.get_rect()
        cps_box.left = 5
        cps_box.centery = 20
        surface.blit(cps_render, cps_box)

        cookies_render = self._font.render("Cookies: %d" % self.cookies, True, (255,255,255))
        cookies_box = cookies_render.get_rect()
        cookies_box.center = surface.get_rect().center
        cookies_box.centery = 20
        surface.blit(cookies_render, cookies_box)


class TheDonut:
    def __init__(self):
        image_file = "donut.png"
        self.img = pygame.image.load(image_file)


def main():
    pygame.init()
#   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    app_name = "Rockwell's Uninformed Tidemark"
    pygame.display.set_caption(app_name)

    clock = pygame.time.Clock()

    lifetime, current, buildings, upgrades, xupgrades = ex1.setup()

    x_widget = XWidget()

    running = True
    ticks = 0
    while running:
        ticks += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                current["buildings"]["b1"] += 1

        cps = ex1.calc_cps(current, buildings, upgrades, xupgrades)
        current["cps"] = cps
        current["cookies"] = current["cookies"] + cps * 1 / float(TICK)
        lifetime["cookies"] = lifetime["cookies"] + cps * 1 / float(TICK)
        status = ex1.get_status(ticks, current)
        print >>sys.stderr, ("\r"+status),

        screen.fill(THECOLORS["blue"])

        x_widget.cps = current["cps"]
        x_widget.cookies = current["cookies"]
        x_widget.draw(screen)

        pygame.display.flip()
        ms_elapsed = clock.tick(TICK)

#       timer.update((ms_elapsed/1000.0)*TICK) # FINISH: does flip() returns the elapsed ti
#       finish_timer.update((ms_elapsed/1000.0)*TICK) # FINISH: does flip() returns the ela
        pygame.event.pump()



if __name__ == '__main__':
    GAMEDIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    sys.exit(main())
