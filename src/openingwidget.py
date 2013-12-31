"""
This is the screen shown while the game is loading.

"""
from common import *
from fonts import Fonts



class OpeningWidget:
    def __init__(self):
        self.timer = 0.0
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        background_img = pygame.image.load(os.path.join(GAMEDIR, BACKGROUND_IMAGE)).convert_alpha()
        background_img = pygame.transform.smoothscale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        background_box = background_img.get_rect()
        background_box.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        donut_img = pygame.image.load(os.path.join(GAMEDIR, TITLE_DONUT_IMAGE)).convert_alpha()
        donut_img = pygame.transform.smoothscale(donut_img, (320, 320))
        donut_box = donut_img.get_rect()
        donut_box.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        text = "Rockwell's Uninformed Tidemark"
        font = "f40"
        antialias = True
        color = "white"
        text_render = getattr(Fonts, font).render(text, antialias, THECOLORS[color])
        text_box = text_render.get_rect()
        text_box.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        surface.blit(background_img, background_box)
        surface.blit(donut_img, donut_box)
        surface.blit(text_render, text_box)

        self.surface = surface

    def draw(self, surface):
        surface.blit(self.surface, (0,0) )

    def on_click(self, pos):
        return True

    def update(self, elapsed):
        if self.timer > 0.0:
            self.timer -= elapsed

