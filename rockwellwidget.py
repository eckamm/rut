from common import *


class RockwellWidget:
    def __init__(self):
        self._load_images()

    def _load_images(self):
        img = pygame.image.load(os.path.join(GAMEDIR, ROCKWELL_IMAGE)).convert_alpha()
        self.img = pygame.transform.smoothscale(img, (200, 120))
        self.box = self.img.get_rect()
        self.box.bottomleft = (0, SCREEN_HEIGHT)

    def draw(self, surface):
        surface.blit(self.img, self.box)
