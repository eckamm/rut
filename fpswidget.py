from common import *
from fonts import Fonts


class FPSWidget:
    def __init__(self):
        self.fps = 0.0
        self.box1 = pygame.Rect(0, 0, 1, 1)

    def update(self, fps):
        self.fps = fps

    def on_click(self, pos):
        if self.box1.collidepoint(pos):
            return True

    def draw(self, surface):
        antialias = False
        render = make_text(Fonts.f15, "%5.2f fps" % (self.fps,), antialias, THECOLORS["white"], TEXT_BACKGROUND)
        self.box1 = render.get_rect()
        self.box1.bottomleft = (0, SCREEN_HEIGHT)
        surface.blit(render, self.box1)


