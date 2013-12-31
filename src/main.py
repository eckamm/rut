try:
    import android
except ImportError:
    android = None


try:
    import pygame.mixer as mixer
    mixer.init()
except ImportError:
    import android.mixer as mixer


import os
import sys
os.environ["GAMEDIR"] = os.path.dirname(os.path.abspath(sys.argv[0]))



import random

from common import *
from fonts import Fonts
import ex1 
from backgroundwidget import BackgroundWidget
from statswidget import StatsWidget
from creditswidget import CreditsWidget
from buttonwidget import ButtonWidget
from fpswidget import FPSWidget
from goldenwidget import GoldenWidget
from donutwidget import DonutWidget
from hudwidget import HUDWidget
from buildingswidget import BuildingsWidget
from resetwidget import ResetWidget
from opening_scene import opening_scene
from profiles_scene import profiles_scene

import pygame.transform



class TheUpgrades:
    def __init__(self, upgrades, buildings, images):
        self.upgrades = upgrades
        self.buildings = buildings
        self.images = images
        self.boxes = []

        self.ximages = {}
        for upgrade_id in sorted(upgrades.keys()):
            filenm = os.path.join(GAMEDIR, IMAGE_DIR, "upgrade-%s.png" % (upgrade_id[:-1],))
            filenm = filenm.replace("*", "ASTERISK")
            self.ximages[upgrade_id[:-1]] = pygame.image.load(filenm).convert_alpha()

        ctrl = [
            ("bought", THECOLORS["black"], 0),
            #("buyable", THECOLORS["green"], 128),
            ("buyable", (32, 128, 32), 128),
            ("available", (200, 32, 32), 200),
            ("unavailable", THECOLORS["black"], 120),
        ]
        self.alphas = {}
        for kind, color, alpha in ctrl:
            self.alphas[kind] = pygame.Surface((40, 40))
            self.alphas[kind].fill(color)
            self.alphas[kind].set_alpha(alpha)

    def update(self, current):
        self.current = current

    def draw(self, surface):
        buyable = ex1.get_buyable_upgrades(self.current, self.upgrades, can_buy=True)
        buyable2 = ex1.get_buyable_upgrades(self.current, self.upgrades, can_buy=False)
        per_row = 10
        init_left = SCREEN_WIDTH - 40 * per_row
        init_centery = 20
        left = init_left
        self.boxes = []
        for idx, upgrade_id in enumerate(self.upgrades.order):
            row = (idx // per_row)
            col = (idx % per_row)

            img = self.ximages[upgrade_id[:-1]]

            box = img.get_rect()
            box.left = init_left + col * box.width
            box.centery = init_centery + row * box.height

            surface.blit(img, box)

            if self.current["upgrades"][upgrade_id]:
                img = self.alphas["bought"]
            elif upgrade_id in buyable:
                img = self.alphas["buyable"]
            elif upgrade_id in buyable2:
                img = self.alphas["available"]
            else:
                img = self.alphas["unavailable"]
            surface.blit(img, box)

            self.boxes.append(box)

    def on_click(self, pos):
        upgrade_ids = self.upgrades.order
        for box, upgrade_id in zip(self.boxes, upgrade_ids):
            if box.collidepoint(pos):
                ex1.buy_upgrade(self.current, self.upgrades, upgrade_id)
                return True

    def on_mouseover(self, pos, rollover_widget):
        upgrade_ids = self.upgrades.order
        for box, upgrade_id in zip(self.boxes, upgrade_ids):
            if box.collidepoint(pos):
                text = ex1.get_upgrade_text(self.current, self.upgrades, self.buildings, upgrade_id)
                rollover_widget.update(text)



class RolloverWidget:
    def __init__(self):
        self.line1 = "."
        self.line2 = "."
        self.update("\n")

    def update(self, text):
        line1, line2 = text.split("\n", 1)
        if line1 == self.line1 and line2 == self.line2:
            return

        self.line1 = line1
        self.line2 = line2

        self.line2_render = make_text(Fonts.f15, self.line2, TEXT_ANTIALIAS, (155, 155, 155), TEXT_BACKGROUND)
        self.line2_box = self.line2_render.get_rect()
        self.line2_box.bottom = SCREEN_HEIGHT - 10
        self.line2_box.centerx = SCREEN_WIDTH / 2

        self.line1_render = make_text(Fonts.f15, self.line1, TEXT_ANTIALIAS, TEXT_COLOR, TEXT_BACKGROUND)
        self.line1_box = self.line1_render.get_rect()
        self.line1_box.bottom = self.line2_box.top - 10
        self.line1_box.centerx = SCREEN_WIDTH / 2

    def draw(self, surface):
        surface.blit(self.line1_render, self.line1_box)
        surface.blit(self.line2_render, self.line2_box)


def main2():
    pygame.init()
    if not android:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DISPLAY_FLAGS, 32)
    else:
        screen = pygame.display.set_mode((0, 0))
        w, h = screen.get_size()
        print "Native resolution:", (w, h)
#       w = w / 2
#       h = h / 2
#       print "Set resolution:", (w, h)
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DISPLAY_FLAGS, 32)
#       screen = pygame.display.set_mode((w, h))
        print "2:Set resolution:", screen.get_size()
    screen.fill(THECOLORS["black"])
    app_name = "Rockwell's Uninformed Tidemark"
    pygame.display.set_caption(app_name)

    quit_game = opening_scene(screen)
    if quit_game:
        running = False
    else:
        running = True

#   images = Images()

    rules_filenm = os.path.join(GAMEDIR, "params.json")
    if android:
        save_filenm = os.path.join(GAMEDIR, "savegame.json")
    else:
        save_filenm = os.path.join(os.path.expanduser("~"), "rut-savegame.json")
        print "@@@", save_filenm

    save_jdat, buildings, upgrades, xupgrades = ex1.setup(save_filenm, "params.json")

    while running:

        profile_id = profiles_scene(screen, save_jdat)
        if profile_id is None:
            running = False

        if running:
            do_quit = game_scene(screen, None, profile_id, save_jdat, save_filenm, buildings, upgrades, xupgrades)
            if do_quit:
                running = False





def game_scene(screen, images, profile_id, save_jdat, save_filenm, buildings, upgrades, xupgrades):

    lifetime = save_jdat["profiles"][profile_id]["lifetime"]
    current = save_jdat["profiles"][profile_id]["current"]
    timing = save_jdat["profiles"][profile_id]["timing"]

    golden = ex1.GoldenModel(current["golden"])

    # Must do startup() to handle background accumulation.
    ex1.startup(timing, lifetime, current, buildings, upgrades, xupgrades)

    background_widget = BackgroundWidget()
    fps_widget = FPSWidget()
    hud_widget = HUDWidget()
    donut_widget = DonutWidget()
#   buildings_widget = TheBuildings(buildings)
    buildings_widget = BuildingsWidget(buildings)
    upgrades_widget = TheUpgrades(upgrades, buildings, images)
    rollover_widget = RolloverWidget()
    golden_widget = GoldenWidget()
    stats_widget = StatsWidget()
    credits_widget = CreditsWidget()
    reset_widget = ResetWidget()


    credits_button_widget = ButtonWidget(BUTTON_CREDITS_IMAGE)
    tmp = credits_button_widget.box
    tmp.centerx = SCREEN_WIDTH//2 + 30
    tmp.top = 0
    credits_button_widget.box = tmp

    reset_button_widget = ButtonWidget(BUTTON_RESET_IMAGE)
    tmp = reset_button_widget.box
    tmp.right = credits_button_widget.box.left - 5
    reset_button_widget.box = tmp

    stats_button_widget = ButtonWidget(BUTTON_STATS_IMAGE)
    tmp = stats_button_widget.box
    tmp.right = reset_button_widget.box.left - 5
    stats_button_widget.box = tmp

    profiles_button_widget = ButtonWidget(BUTTON_PROFILES_IMAGE)
    tmp = profiles_button_widget.box
    tmp.right = stats_button_widget.box.left - 5
    profiles_button_widget.box = tmp



    font_set_idx = 0
    Fonts.activate_font_set(font_set_idx)

    ticks = 0
    running = True
    clock = pygame.time.Clock()
    ms_elapsed = 0.0
    do_quit = False
    while running:
        ticks += 1

        if android:
            if android.check_pause():
                print "@@@@ pausing"
                running = False
               ## Save the game state to a file.
               #with open(save_filenm, "w") as fp:
               #    json.dump(save_jdat, fp, indent=4)
               #android.wait_for_resume()
               #print "@@@@ resuming"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                do_quit = True
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                do_quit = True
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                stats_widget.showing = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                credits_widget.showing = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                background_widget._load_images()
                donut_widget._load_images()
                buildings_widget._load_images()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                font_set_idx = (font_set_idx + 1) % len(Fonts.font_sets)
                Fonts.activate_font_set(font_set_idx)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                from fmt import fmt as xxfmt
                xxfmt.next()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                # Removing this key action will also disable the Android "back" button.
                do_quit = False
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                current["cookies"] += 100000000000000000
                current["game_cookies"] += 100000000000000000
                lifetime["cookies"] += 100000000000000000

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                ex1.soft_reset(save_jdat["profiles"], profile_id, buildings, upgrades)
                # save_jdat["profiles"]["current"] has been replaced; need to update pointer
                current = save_jdat["profiles"][profile_id]["current"]

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFTBUTTON:
                # Note that the on_click() methods do their own click detection and
                # return True when the click was on the owning object.
                if stats_widget.on_click(event.pos):
                    pass
                elif credits_widget.on_click(event.pos):
                    pass
                elif golden_widget.on_click(event.pos):
                    pass
                elif donut_widget.on_click(event.pos):
                    # FINISH: put a function in ex1 to do this type of thing
                    current["cookies"] += current["cpc"]
                    current["game_cookies"] += current["cpc"]
                    lifetime["cookies"] += current["cpc"]
                elif credits_button_widget.on_click(event.pos):
                    credits_widget.showing = True
                elif stats_button_widget.on_click(event.pos):
                    stats_widget.showing = True
                elif profiles_button_widget.on_click(event.pos):
                    do_quit = False
                    running = False
                elif buildings_widget.on_click(event.pos):
                    pass
                elif upgrades_widget.on_click(event.pos):
                    pass
                elif reset_button_widget.on_click(event.pos):
                    ex1.soft_reset(save_jdat["profiles"], profile_id, buildings, upgrades)
                    current = save_jdat["profiles"][profile_id]["current"]

            elif event.type == pygame.MOUSEMOTION:
                buildings_widget.on_mouseover(event.pos, rollover_widget)
                upgrades_widget.on_mouseover(event.pos, rollover_widget)

        # FINISH: make functions in ex1 which do all this work.
        # ex1.update_state(lifetime, current, elapsed)
        # ex1.calc_aux(lifetime, current) -> building_status, upgrade_status, golden_status?
        elapsed = ms_elapsed/1000.0
        ex1.update_state(elapsed, timing, lifetime, current, buildings, upgrades, xupgrades)
        golden.update(elapsed)
        donut_widget.update(elapsed)
        stats_widget.update(lifetime, current, timing)
        reset_widget.update(ex1.get_shard_value(save_jdat["profiles"], profile_id))
        credits_button_widget.update(elapsed)
        reset_button_widget.update(elapsed)
        stats_button_widget.update(elapsed)
        profiles_button_widget.update(elapsed)

        building_costs = ex1.current_costs(current, buildings)

        # FINISH: make a HUDWidget.update() method.  Rename HUDWidget.
        hud_widget.cps = current["cps"]
        hud_widget.cpc = current["cpc"]
        hud_widget.cookies = current["cookies"]
        hud_widget.game_cookies = current["game_cookies"]

        buildings_widget.update(current, building_costs)
        upgrades_widget.update(current)
        golden_widget.update(golden)

        if MODE==2:
            #screen.fill(THECOLORS["black"])
            background_widget.draw(screen)
        else:
            background_widget.draw(screen)
        hud_widget.draw(screen)
        buildings_widget.draw(screen)
        upgrades_widget.draw(screen)
        donut_widget.draw(screen)
        rollover_widget.draw(screen)
        if DEBUG:
            fps_widget.draw(screen)
        credits_button_widget.draw(screen)
        reset_button_widget.draw(screen)
        stats_button_widget.draw(screen)
        profiles_button_widget.draw(screen)

        golden_widget.draw(screen)
        stats_widget.draw(screen)
        credits_widget.draw(screen)
        reset_widget.draw(screen)

        pygame.display.flip()
        ms_elapsed = clock.tick(TICK)
        fps_widget.update(clock.get_fps())

#       timer.update((ms_elapsed/1000.0)*TICK) # FINISH: does flip() returns the elapsed ti
#       finish_timer.update((ms_elapsed/1000.0)*TICK) # FINISH: does flip() returns the ela
        pygame.event.pump()


    # Must do shutdown() to prep for background accumulation.
    ex1.shutdown(timing)

    # Save the game state to a file.
    with open(save_filenm, "w") as fp:
        json.dump(save_jdat, fp, indent=4)

    return do_quit


def main():
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_p)

    GAMEDIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    if os.environ.get("PROFILE", "") == "1":
        import profile
        profile.run("main2()")
    else:
        sys.exit(main2())


if __name__ == '__main__':
    main()
