from common import *
from fonts import Fonts


class ResetWidget:
    """
    waiting -> nothing
    available -> display in random place on screen
    available and active -> display name and effect under big donut
    """
    def __init__(self):
        self.shards = 0

    def update(self, shards):
        self.shards = shards

    def draw(self, surface):
        antialias = False
        render = make_text(Fonts.f15, "Soft Reset Worth: %s" % fmt(self.shards), antialias, THECOLORS["white"], TEXT_BACKGROUND)
        self.box = render.get_rect()
        self.box.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)
        surface.blit(render, self.box)

    def on_click(self, pos):
        if self.box.collidepoint(pos):
            return True
