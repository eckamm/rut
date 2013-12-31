try:
    import android
except ImportError:
    android = None

from common import *

from openingwidget import OpeningWidget
from versionwidget import VersionWidget
from rockwellwidget import RockwellWidget


def opening_scene(screen):
    pygame.display.flip()
    opening_widget = OpeningWidget()
    version_widget = VersionWidget()
    rockwell_widget = RockwellWidget()
    clock = pygame.time.Clock()
    running = True
    while running:

        if android:
            if android.check_pause():
                print "@@@@ pausing"
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_game = True
            elif ( event.type == pygame.MOUSEBUTTONDOWN or
                   event.type == pygame.KEYDOWN ):
                running = False
                quit_game = False
        ms_elapsed = clock.tick(TICK)
        pygame.event.pump()
        opening_widget.draw(screen)
        version_widget.draw(screen)
        rockwell_widget.draw(screen)
        pygame.display.flip()
    return quit_game
