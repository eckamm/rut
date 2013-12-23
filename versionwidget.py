from common import *
from fonts import Fonts


class VersionWidget:
    def __init__(self):
        antialias = True
        self.render = make_text(Fonts.f15, "Version %s" % (VERSION,), antialias, THECOLORS["white"], TEXT_BACKGROUND)
        self.box = self.render.get_rect()
        self.box.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)

    def draw(self, surface):
        surface.blit(self.render, self.box)


