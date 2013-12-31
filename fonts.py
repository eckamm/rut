import os

import pygame.font
pygame.font.init()


GAMEDIR = os.environ["GAMEDIR"]
FONTDIR = os.path.join(GAMEDIR, "fonts")
FONT1_FILE = os.path.join(FONTDIR, "Chunk.ttf")
FONT2_FILE = os.path.join(FONTDIR, "Munro.ttf")
FONT3_FILE = os.path.join(FONTDIR, "MunroNarrow.ttf")
FONT4_FILE = os.path.join(FONTDIR, "MunroSmall.ttf")
FONT5_FILE = os.path.join(FONTDIR, "aesymatt.ttf")
FONT6_FILE = os.path.join(FONTDIR, "Arcade.ttf")
FONT7_FILE = os.path.join(FONTDIR, "knewave.ttf")



class _Fonts:
    def __init__(self):
        self.font_sets = []
        for kind in [FONT1_FILE, FONT2_FILE, FONT3_FILE, FONT4_FILE, FONT5_FILE, FONT6_FILE, FONT7_FILE]:
            self.font_sets.append({
                "f15": pygame.font.Font(os.path.join(GAMEDIR, kind), 15),
                "f12": pygame.font.Font(os.path.join(GAMEDIR, kind), 12),
                "f18": pygame.font.Font(os.path.join(GAMEDIR, kind), 18),
                "f20": pygame.font.Font(os.path.join(GAMEDIR, kind), 20),
                "f25": pygame.font.Font(os.path.join(GAMEDIR, kind), 25),
                "f30": pygame.font.Font(os.path.join(GAMEDIR, kind), 30),
                "f35": pygame.font.Font(os.path.join(GAMEDIR, kind), 35),
                "f40": pygame.font.Font(os.path.join(GAMEDIR, kind), 40),
                "f80": pygame.font.Font(os.path.join(GAMEDIR, kind), 80),
            })
        self.activate_font_set(0)

    def activate_font_set(self, idx):
        for k, v in self.font_sets[idx].iteritems():
            setattr(self, k, v)


Fonts = _Fonts()



