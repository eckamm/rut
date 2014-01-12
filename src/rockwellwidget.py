from common import *
from fonts import Fonts


class RockwellWidget:
    def __init__(self):
        self._load_images()

        antialias = True
        self.text_render = make_text(Fonts.f15, "Rockwell Game Studio", antialias, THECOLORS["white"], TEXT_BACKGROUND)
        self.text_box = self.text_render.get_rect()
        self.text_box.bottomleft = self.box.bottomright

    def _load_images(self):
        img = pygame.image.load(os.path.join(GAMEDIR, ROCKWELL_IMAGE)).convert_alpha()
        self.img = pygame.transform.smoothscale(img, (120, 120))
        self.box = self.img.get_rect()
        self.box.bottomleft = (0, SCREEN_HEIGHT)

    def draw(self, surface):
        surface.blit(self.img, self.box)
        surface.blit(self.text_render, self.text_box)
