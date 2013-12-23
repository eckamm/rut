"""
This is an overlay box with some statistics in it which is shown
when a button is clicked and goes away when the screen is clicked.

"""
import datetime

from common import *
from fonts import Fonts


"""
name
current cookies
current game_cookies
current cpc
current cps
lifetime cookies
lifetime bg_cookies
lifetime shards
timing bg_seconds
timing fg_seconds
"""


def sfmt(secs):
    rest, ss = divmod(secs, 60)
    rest, mm = divmod(rest, 60)
    rest, hh = divmod(rest, 24)
    ww, dd = divmod(rest, 7)
    return "%.0fw %.0fd %.0fh %.0fm %.0fs" % (ww, dd, hh, mm, ss)


class StatsWidget:
#   bg_color = THECOLORS["brown"]
    bg_color = (THECOLORS["brown"][0], THECOLORS["brown"][1], THECOLORS["brown"][2], 128+64)

    def __init__(self):
        self.showing = False

    def update(self, lifetime, current, timing):
        """
        """
        self.lifetime = lifetime
        self.current = current
        self.timing = timing

    def draw(self, surface):
        """
        """
        if self.showing:
            self._draw(surface)

    def _draw_bg(self, surface):
#       self.bg_surface = pygame.Surface((int(0.8*SCREEN_WIDTH), int(0.8*SCREEN_HEIGHT)))
#       self.bg_surface.set_alpha(128)
        #self.bg_surface = pygame.Surface((int(0.8*SCREEN_WIDTH), int(0.8*SCREEN_HEIGHT)), pygame.SRCALPHA)
        self.bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.bg_surface.fill(self.bg_color)
        self.bg_box = self.bg_surface.get_rect()
        self.bg_box.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        surface.blit(self.bg_surface, self.bg_box)
 

    def _draw(self, surface):

        CTRL = []
        CTRL.append(("Current", "f35", "white"))
        CTRL.append(("DPS: %s" % fmt(self.current["cps"]), "f25", "white"))
        CTRL.append(("DPC: %s" % fmt(self.current["cpc"]), "f25", "white"))
        CTRL.append(("Donuts: %s" % fmt(self.current["cookies"]), "f25", "white"))
        CTRL.append(("Total Donuts: %s" % fmt(self.current["game_cookies"]), "f25", "white"))

        CTRL.append(("", "f15", "white"))
        CTRL.append(("Lifetime", "f35", "white"))
        CTRL.append(("Shards: %s" % fmt(self.lifetime["shards"]), "f25", "white"))
        CTRL.append(("Donuts: %s" % fmt(self.lifetime["cookies"]), "f25", "white"))
        CTRL.append(("Foreground Donuts: %s" % fmt(self.lifetime["cookies"]-self.lifetime["bg_cookies"]), "f25", "white"))
        CTRL.append(("Background Donuts: %s" % fmt(self.lifetime["bg_cookies"]), "f25", "white"))

        CTRL.append(("", "f15", "white"))
        CTRL.append(("Time", "f35", "white"))
        CTRL.append(("Start: %s" % (datetime.datetime.fromtimestamp(self.timing["initial_ts"]).strftime("%Y-%m-%d %H:%M:%S"),), "f25", "white"))
        CTRL.append(("Foreground: %s" % sfmt(self.timing["fg_seconds"]), "f25", "white"))
        CTRL.append(("Background: %s" % sfmt(self.timing["bg_seconds"]), "f25", "white"))

        self._draw_bg(surface)
        y = self.bg_box.top + 30
        x = SCREEN_WIDTH / 2
        antialias = False
        for text, font, color in CTRL:
            if ":" not in text:
                render = getattr(Fonts, font).render(text, antialias, THECOLORS[color])
                box = render.get_rect()
                box.centerx = x
                box.top = y
                surface.blit(render, box)
                y = box.bottom + 5
                continue

            text1, text2 = text.split(":", 1)
            text1 += ":"

            render = getattr(Fonts, font).render(text1, antialias, THECOLORS[color])
            box = render.get_rect()
            box.right = x
            box.top = y
            surface.blit(render, box)

            render = getattr(Fonts, font).render(text2, antialias, THECOLORS[color])
            box = render.get_rect()
            box.left = x
            box.top = y
            surface.blit(render, box)

            y = box.bottom + 5

        return
 
        self._draw_bg(surface)
        y = self.bg_box.top + 30
        x = SCREEN_WIDTH / 2
        antialias = False
        for text, font, color in CTRL:
            render = getattr(Fonts, font).render(text, antialias, THECOLORS[color])
            box = render.get_rect()
            box.centerx = x
            box.top = y
            surface.blit(render, box)
            y = box.bottom + 5
        return


    def on_click(self, pos):
        # A click anywhere closes the stats display.
        if self.showing:
            self.showing = False
            return True


