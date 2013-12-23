from common import *
from fonts import Fonts


class HUDWidget:
    def __init__(self):
        self.cps = 0
        self.cpc = 1
        self.cookies = 0
        self.game_cookies = 0

    def draw(self, surface):
#       TEXT_COLOR = (255, 255, 51) #THECOLORS["yellow"]
#       TEXT_COLOR = (33, 50, 64) #THECOLORS["yellow"]
        cps_render = make_text(Fonts.f15, "DPS: %s" % fmt(self.cps), TEXT_ANTIALIAS, TEXT_COLOR, TEXT_BACKGROUND)
        cps_box = cps_render.get_rect()
        if MODE==2:
            cps_box.left = SCREEN_WIDTH - 400
            cps_box.centery = 0.74 * SCREEN_HEIGHT
        else:
            cps_box.left = 10
            cps_box.centery = 20
        surface.blit(cps_render, cps_box)

        cpc_render = make_text(Fonts.f15, "DPC: %s" % fmt(self.cpc), TEXT_ANTIALIAS, TEXT_COLOR, TEXT_BACKGROUND)
        cpc_box = cpc_render.get_rect()
        cpc_box.left = cps_box.left
        cpc_box.top = cps_box.bottom + 10
        surface.blit(cpc_render, cpc_box)

        cookies_render = make_text(Fonts.f15, "Donuts: %s" % fmt(self.cookies), TEXT_ANTIALIAS, TEXT_COLOR, TEXT_BACKGROUND)
        cookies_box = cookies_render.get_rect()
        cookies_box.left = cpc_box.left
        cookies_box.top = cpc_box.bottom + 10
        surface.blit(cookies_render, cookies_box)
        
        game_cookies_render = make_text(Fonts.f15, "Total Donuts: %s" % fmt(self.game_cookies), TEXT_ANTIALIAS, TEXT_COLOR, TEXT_BACKGROUND)
        game_cookies_box = game_cookies_render.get_rect()
        game_cookies_box.left = cookies_box.left
        game_cookies_box.top = cookies_box.bottom + 10
        surface.blit(game_cookies_render, game_cookies_box)


