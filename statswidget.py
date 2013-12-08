"""
This is an overlay box with some statistics in it which is shown
when a button is clicked and goes away when the screen is clicked.
"""
from common import *


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
def _f(self, lifetime, current):
    self._font.render
    cpc_render = self._font.render("DPC: %s" % fmt(self.cpc), True, TEXT_COLOR)



class StatsWidget:
#   bg_color = THECOLORS["brown"]
    bg_color = (THECOLORS["brown"][0], THECOLORS["brown"][1], THECOLORS["brown"][2], 128)

    def __init__(self):
        self.showing = False
        self.cps = 0
        self.cpc = 1
        self.cookies = 0
        self.game_cookies = 0
        self._font = pygame.font.SysFont(None, 15)

    def update(self, lifetime, current):
        """
        """
        self.lifetime = lifetime
        self.current = current

    def draw(self, surface):
        """
        """
        if self.showing:
            self._draw(surface)

    def _draw_bg(self, surface):
#       self.bg_surface = pygame.Surface((int(0.8*SCREEN_WIDTH), int(0.8*SCREEN_HEIGHT)))
#       self.bg_surface.set_alpha(128)
        self.bg_surface = pygame.Surface((int(0.8*SCREEN_WIDTH), int(0.8*SCREEN_HEIGHT)), pygame.SRCALPHA)
        self.bg_surface.fill(self.bg_color)
        self.bg_box = self.bg_surface.get_rect()
        self.bg_box.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        surface.blit(self.bg_surface, self.bg_box)
        

    def _draw(self, surface):
        self._draw_bg(surface)
        return

        cps_render = self._font.render("DPS: %s" % fmt(self.cps), True, (255,255,255))
        cps_box = cps_render.get_rect()
        cps_box.left = 10
        cps_box.centery = 20
        surface.blit(cps_render, cps_box)

        cpc_render = self._font.render("DPC: %s" % fmt(self.cpc), True, (255,255,255))
        cpc_box = cpc_render.get_rect()
        cpc_box.left = 10
        cpc_box.top = cps_box.bottom + 10
        surface.blit(cpc_render, cpc_box)

        cookies_render = self._font.render("Donuts: %s" % fmt(self.cookies), True, (255,255,255))
        cookies_box = cookies_render.get_rect()
        cookies_box.left = 10
        cookies_box.top = cpc_box.bottom + 10
        surface.blit(cookies_render, cookies_box)

        game_cookies_render = self._font.render("Total Donuts: %s" % fmt(self.game_cookies), True, (255,255,255))
        game_cookies_box = game_cookies_render.get_rect()
        game_cookies_box.left = 10
        game_cookies_box.top = cookies_box.bottom + 10
        surface.blit(game_cookies_render, game_cookies_box)

    def on_click(self, pos):
        # A click anywhere closes the stats display.
        if self.showing:
            self.showing = False
            return True


