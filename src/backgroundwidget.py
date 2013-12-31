from common import *


class BackgroundWidget:
    def __init__(self):
        self._load_images()

    def _load_images(self):
        img = pygame.image.load(os.path.join(GAMEDIR, BACKGROUND_IMAGE)).convert_alpha()
        self.img = pygame.transform.smoothscale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.box = self.img.get_rect()
        self.box.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    def draw(self, surface):
        surface.blit(self.img, self.box)
