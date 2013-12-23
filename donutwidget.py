from common import *


class DonutWidget:
    def __init__(self):
        self._load_images()
        self.timer = 0.0

    def _load_images(self):
        image_file = DONUT_IMAGE
        self.img1 = pygame.image.load(os.path.join(GAMEDIR, image_file)).convert_alpha()
        self.img1 = pygame.transform.smoothscale(self.img1, (256, 256))
        self.box1 = self.img1.get_rect()
        if MODE==2:
            self.box1.center = (0.4*SCREEN_WIDTH, 0.36*SCREEN_HEIGHT)
        else:
            self.box1.center = (SCREEN_WIDTH/7, SCREEN_HEIGHT/2)
        image_file = DONUT_CLICKED_IMAGE
        self.img2 = pygame.image.load(os.path.join(GAMEDIR, image_file)).convert_alpha()
        self.img2 = pygame.transform.smoothscale(self.img2, (240, 240))
        self.box2 = self.img2.get_rect()
        if MODE==2:
            self.box2.center = (0.4*SCREEN_WIDTH, 0.36*SCREEN_HEIGHT)
        else:
            self.box2.center = (SCREEN_WIDTH/7, SCREEN_HEIGHT/2)

    def update(self, elapsed):
        if self.timer > 0.0:
            self.timer -= elapsed

    def on_click(self, pos):
        if self.box1.collidepoint(pos):
            if self.timer <= 0.0:
                self.timer = 0.16
            return True

    def draw(self, surface):
        if self.timer <= 0.0:
            # normal
            surface.blit(self.img1, self.box1)
        else:
            # pressed
            surface.blit(self.img2, self.box2)


