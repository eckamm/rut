import os

import pygame.font
pygame.font.init()


GAMEDIR = os.environ["GAMEDIR"]
FONTDIR = os.path.join(GAMEDIR, "fonts")
FONT1_FILE = os.path.join(FONTDIR, "Munro.ttf")
FONT2_FILE = os.path.join(FONTDIR, "MunroNarrow.ttf")
FONT3_FILE = os.path.join(FONTDIR, "MunroSmall.ttf")
FONT4_FILE = os.path.join(FONTDIR, "aesymatt.ttf")
FONT5_FILE = os.path.join(FONTDIR, "Arcade.ttf")



class _Fonts:
    def __init__(self):
        self.font_sets = []
        for kind in [FONT1_FILE, FONT2_FILE, FONT3_FILE, FONT4_FILE, FONT5_FILE]:
            self.font_sets.append({
                "f15": pygame.font.Font(os.path.join(GAMEDIR, kind), 15),
                "f20": pygame.font.Font(os.path.join(GAMEDIR, kind), 20),
                "f30": pygame.font.Font(os.path.join(GAMEDIR, kind), 30),
            })
        self.activate_font_set(0)

    def activate_font_set(self, idx):
        self.f15 = self.font_sets[idx]["f15"]
        self.f20 = self.font_sets[idx]["f20"]
        self.f30 = self.font_sets[idx]["f30"]


Fonts = _Fonts()

