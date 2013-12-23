import random

from common import *
from fonts import Fonts



class GoldenWidget:
    """
    waiting -> nothing
    available -> display in random place on screen
    available and active -> display name and effect under big donut
    """
    def __init__(self):
        image_file = GOLDEN_AVAILABLE_IMAGE
        self.available_img = pygame.image.load(os.path.join(GAMEDIR, image_file)).convert_alpha()
        self.available_img = pygame.transform.smoothscale(self.available_img, (40, 40))
        self.available_box = self.available_img.get_rect()
        self.available_box.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        image_file = GOLDEN_ACTIVE_IMAGE
        self.active_img = pygame.image.load(os.path.join(GAMEDIR, image_file)).convert_alpha()
        self.active_img = pygame.transform.smoothscale(self.active_img, (40, 40))
        self.active_box = self.active_img.get_rect()
        if MODE==2:
            self.active_box.center = (0.4*SCREEN_WIDTH, 0.6*SCREEN_HEIGHT)
        else:
            self.active_box.center = (SCREEN_WIDTH/7, 4*SCREEN_HEIGHT/5)
        self.last_state = ("", False)  # state, active

    def _pick_random_pos(self):
        w_margin = SCREEN_WIDTH//20
        h_margin = SCREEN_HEIGHT//20
        x = w_margin + random.randrange(SCREEN_WIDTH-2*w_margin)
        y = h_margin + random.randrange(SCREEN_HEIGHT-2*h_margin)
        return x, y

    def update(self, golden):
        self.golden = golden
        if self.last_state == (self.golden.data["state"], self.golden.data["active"]):
            return
        # Track the last state for the next call.
        self.last_state = (golden.data["state"], golden.data["active"])
        # There was a state transition, so pick a new random location for next golden.
        self.available_box.center = self._pick_random_pos()
        if self.golden.data["state"] == "waiting":
            # Draw will do nothing during waiting state.
            self.draw = lambda x:None
        elif self.golden.data["state"] == "available" and not self.golden.data["active"]:
            self.draw = self._draw_avail
        elif self.golden.data["state"] == "available" and self.golden.data["active"]:
            self.draw = self._draw_active
            # Prep the text for the current golden.
            rule = self.golden.get_ctrl()
            self.text_render = make_text(Fonts.f15, "%s" % (rule["name"],), TEXT_ANTIALIAS, (0, 255, 0), TEXT_BACKGROUND)
            self.text_box = self.text_render.get_rect()
            self.text_box.top = self.active_box.bottom
            self.text_box.centerx = self.active_box.centerx

    def _draw_avail(self, surface):
        surface.blit(self.available_img, self.available_box)

    def _draw_active(self, surface):
        surface.blit(self.active_img, self.active_box)
        surface.blit(self.text_render, self.text_box)

    def on_click(self, pos):
        if not hasattr(self, "golden"):
            return
        if self.golden.data["state"] != "available":
            return
        if self.available_box.collidepoint(pos):
            self.golden.activate()
            return True

