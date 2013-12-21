from common import *
from fonts import Fonts


class ButtonWidget(object):
    def __init__(self, image_file):
        self.image_file = image_file
        self._load_images()
        self._box = self._box1
        self._timer = 0.0

    def get_box(self):
        return self._box
    def set_box(self, box):
        self._box = box
        self._box1 = self._box
        self._box2.center = self._box1.center
    box = property(get_box, set_box)

    def _load_images(self):
        dims = (147, 46)
        clicked_dims =  (142, 42)
        dims = (2*147//3, 2*46//3)
        clicked_dims =  (2*142//3, 2*42//3)
        self._img1 = pygame.image.load(os.path.join(GAMEDIR, self.image_file)).convert_alpha()
        self._img1 = pygame.transform.smoothscale(self._img1, dims)
        self._box1 = self._img1.get_rect()
        self._img2 = pygame.image.load(os.path.join(GAMEDIR, self.image_file)).convert_alpha()
        self._img2 = pygame.transform.smoothscale(self._img2, clicked_dims)
        self._box2 = self._img2.get_rect()
        self._box2.center = self._box1.center

    def update(self, elapsed):
        if self._timer > 0.0:
            self._timer -= elapsed

    def on_click(self, pos):
        if self._box1.collidepoint(pos):
            if self._timer <= 0.0:
                self._timer = 0.16
            return True

    def draw(self, surface):
        if self._timer <= 0.0:
            # normal
            surface.blit(self._img1, self._box1)
        else:
            # pressed
            surface.blit(self._img2, self._box2)

