"""
This is an overlay box with game credits in it which is shown
when a button is clicked and goes away when the screen is clicked.

"""
from common import *
from fonts import Fonts


CTRL = [
    ["Rockwell's Uninformed Tidemark", "f40", "white"],
    ["Dedicated to Mrs. G / Mom", "f20", "white"],
    ["", "f15", "white"],
    ["Programming", "f30", "white"],
    ["Noah (13)", "f20", "white"],
    ["Eric", "f20", "white"],
    ["", "f30", "white"],
    ["Writing", "f30", "white"],
    ["Noah", "f20", "white"],
    ["", "f30", "white"],
    ["Artwork", "f30", "white"],
    ["Emma (11)", "f20", "white"],
    ["Noah", "f20", "white"],
    ["Eric", "f20", "white"],
    ["", "f30", "white"],
    ["Playtesting", "f30", "white"],
    ["Abe (8)", "f20", "white"],
]


class CreditsWidget:
#   bg_color = THECOLORS["brown"]
    bg_color = (THECOLORS["brown"][0], THECOLORS["brown"][1], THECOLORS["brown"][2], 128)

    def __init__(self):
        self.showing = False

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

        cps_render = Fonts.f15.render("DPS: %s" % fmt(self.cps), True, (255,255,255))
        cps_box = cps_render.get_rect()
        cps_box.left = 10
        cps_box.centery = 20
        surface.blit(cps_render, cps_box)

        cpc_render = Fonts.f15.render("DPC: %s" % fmt(self.cpc), True, (255,255,255))
        cpc_box = cpc_render.get_rect()
        cpc_box.left = 10
        cpc_box.top = cps_box.bottom + 10
        surface.blit(cpc_render, cpc_box)

        cookies_render = Fonts.f15.render("Donuts: %s" % fmt(self.cookies), True, (255,255,255))
        cookies_box = cookies_render.get_rect()
        cookies_box.left = 10
        cookies_box.top = cpc_box.bottom + 10
        surface.blit(cookies_render, cookies_box)

        game_cookies_render = Fonts.f15.render("Total Donuts: %s" % fmt(self.game_cookies), True, (255,255,255))
        game_cookies_box = game_cookies_render.get_rect()
        game_cookies_box.left = 10
        game_cookies_box.top = cookies_box.bottom + 10
        surface.blit(game_cookies_render, game_cookies_box)

    def on_click(self, pos):
        # A click anywhere closes the stats display.
        if self.showing:
            self.showing = False
            return True


