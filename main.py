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
from statswidget import StatsWidget

import pygame.transform


MODE = int(os.environ.get("MODE", 2))

def make_text(font, text):
    """
    returns (text_surface, bg_surface, box)
    """
        

class XWidget:
    def __init__(self):
        self.cps = 0
        self.cpc = 1
        self.cookies = 0
        self.game_cookies = 0

    def draw(self, surface):
        cps_render = Fonts.f15.render("DPS: %s" % fmt(self.cps), TEXT_ANTIALIAS, TEXT_COLOR, TEXT_BACKGROUND)
        cps_box = cps_render.get_rect()
        if MODE==2:
            cps_box.left = SCREEN_WIDTH - 400
            cps_box.centery = 0.74 * SCREEN_HEIGHT
        else:
            cps_box.left = 10
            cps_box.centery = 20
        surface.blit(cps_render, cps_box)

        cpc_render = Fonts.f15.render("DPC: %s" % fmt(self.cpc), TEXT_ANTIALIAS, TEXT_COLOR, TEXT_BACKGROUND)
        cpc_box = cpc_render.get_rect()
        cpc_box.left = cps_box.left
        cpc_box.top = cps_box.bottom + 10
        surface.blit(cpc_render, cpc_box)

        cookies_render = Fonts.f15.render("Donuts: %s" % fmt(self.cookies), TEXT_ANTIALIAS, TEXT_COLOR, TEXT_BACKGROUND)
        cookies_box = cookies_render.get_rect()
        cookies_box.left = cpc_box.left
        cookies_box.top = cpc_box.bottom + 10
        surface.blit(cookies_render, cookies_box)
        
        game_cookies_render = Fonts.f15.render("Total Donuts: %s" % fmt(self.game_cookies), TEXT_ANTIALIAS, TEXT_COLOR, TEXT_BACKGROUND)
        game_cookies_box = game_cookies_render.get_rect()
        game_cookies_box.left = cookies_box.left
        game_cookies_box.top = cookies_box.bottom + 10
        surface.blit(game_cookies_render, game_cookies_box)


class TheDonut:
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
        self.img2 = pygame.transform.smoothscale(self.img2, (256, 256))
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


class FPSWidget:
    def __init__(self):
        self.fps = 0.0

    def update(self, fps):
        self.fps = fps

    def draw(self, surface):
        antialias = False
        render = Fonts.f15.render("%5.2f fps" % (self.fps,), antialias, THECOLORS["white"])
        box = render.get_rect()
        box.bottomleft = (0, SCREEN_HEIGHT)
        surface.blit(render, box)



class TheBuildings:
    def __init__(self, buildings):
        self.buildings = buildings
        self._load_images()
        self.boxes = []

    def _load_images(self):
        self.images = []
        for building_id in sorted(self.buildings.keys()):
            filenm = os.path.join(GAMEDIR, IMAGE_DIR, "building-%s.png" % (building_id,))
            self.images.append(pygame.image.load(filenm).convert_alpha())

    def update(self, current, building_costs):
        self.current = current
        self.building_costs = building_costs

    def draw(self, surface):
        y = self.images[0].get_rect().h//2
        self.boxes = []
        buyable = ex1.get_buyable_buildings(self.current, self.buildings)
        for idx, building_id in enumerate(sorted(self.buildings.keys())):
            if building_id in buyable:
                color = TEXT_COLOR
            else:
                color = THECOLORS["orange"]
            name = self.buildings[building_id].get("name", building_id)
            render = Fonts.f15.render("%s (%d) -- Cost: %s" % (name,
                self.current["buildings"][building_id],
                fmt(self.building_costs[building_id])),
                TEXT_ANTIALIAS, color, TEXT_BACKGROUND)

            box2 = self.images[idx].get_rect()
            box2.centery = y
            if MODE == 2:
                box2.left = 0
            else:
                box2.left = 1.4 * SCREEN_WIDTH / 5
            surface.blit(self.images[idx],box2)

            box = render.get_rect()
            box.left = box2.right
            box.centery = box2.centery
            surface.blit(render, box)

            y += box2.height + 5
            self.boxes.append((box, box2))

    def on_click(self, pos):
        building_ids = sorted(self.buildings.keys())
        for (box1, box2), building_id in zip(self.boxes, building_ids):
            if box1.collidepoint(pos) or box2.collidepoint(pos):
                ex1.buy_building(self.current, self.buildings, building_id)
                return True

    def on_mouseover(self, pos, rollover_widget):
        building_ids = sorted(self.buildings.keys())
        for (box1, box2), building_id in zip(self.boxes, building_ids):
            if box1.collidepoint(pos) or box2.collidepoint(pos):
                text = ex1.get_building_text(self.current, self.buildings, building_id)
                rollover_widget.update(text)



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
            self.text_render = Fonts.f15.render("%s" % (rule["name"],), TEXT_ANTIALIAS, (0, 255, 0), TEXT_BACKGROUND)
            self.text_box = self.text_render.get_rect()
            self.text_box.top = self.active_box.bottom
            self.text_box.centerx = self.active_box.centerx

    def _draw_avail(self, surface):
        surface.blit(self.available_img, self.available_box)

    def _draw_active(self, surface):
        surface.blit(self.active_img, self.active_box)
        surface.blit(self.text_render, self.text_box)

    def on_click(self, pos):
        if self.golden.data["state"] != "available":
            return
        if self.available_box.collidepoint(pos):
            self.golden.activate()
            return True


class ResetWidget:
    """
    waiting -> nothing
    available -> display in random place on screen
    available and active -> display name and effect under big donut
    """
    def __init__(self):
        self.shards = 0
        
    def update(self, shards):
        self.shards = shards
        
    def draw(self, surface):
        antialias = False
        render = Fonts.f15.render("Soft Reset Worth: %s" % self.shards, antialias, THECOLORS["white"])
        self.box = render.get_rect()
        self.box.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)
        surface.blit(render, self.box)

    def on_click(self, pos):
        if self.box.collidepoint(pos):
            return True
  


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
            ("unavailable", THECOLORS["black"], 200),
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

#           if self.current["upgrades"][upgrade_id]:
#               img = self.images.imgs[1]
#           elif upgrade_id in buyable:
#               img = self.images.imgs[0]
#           elif upgrade_id in buyable2:
#               img = self.images.imgs[3]
#           else:
#               img = self.images.imgs[2]
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

        self.line2_render = Fonts.f15.render(self.line2, TEXT_ANTIALIAS, (155, 155, 155), TEXT_BACKGROUND)
        self.line2_box = self.line2_render.get_rect()
        self.line2_box.bottom = SCREEN_HEIGHT - 10
        self.line2_box.centerx = SCREEN_WIDTH / 2

        self.line1_render = Fonts.f15.render(self.line1, TEXT_ANTIALIAS, TEXT_COLOR, TEXT_BACKGROUND)
        self.line1_box = self.line1_render.get_rect()
        self.line1_box.bottom = self.line2_box.top - 10
        self.line1_box.centerx = SCREEN_WIDTH / 2



    def draw(self, surface):
        surface.blit(self.line1_render, self.line1_box)
        surface.blit(self.line2_render, self.line2_box)


class Images:
    def __init__(self):
        nms = [UPGRADE_STATE1_IMAGE, UPGRADE_STATE2_IMAGE, UPGRADE_STATE3_IMAGE, UPGRADE_STATE4_IMAGE]
        self.imgs = []
        for nm in nms:
            image_file = os.path.join(GAMEDIR, nm)
            img = pygame.image.load(image_file).convert_alpha()
            self.imgs.append(img)


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
    app_name = "Rockwell's Uninformed Tidemark"
    pygame.display.set_caption(app_name)

    clock = pygame.time.Clock()
    ms_elapsed = 0.0

    images = Images()

    rules_filenm = os.path.join(GAMEDIR, "params.json")
    save_filenm = os.path.join(GAMEDIR, "savegame.json")
    save_jdat, buildings, upgrades, xupgrades = ex1.setup("savegame.json", "params.json")
    profile_id = 0
    lifetime = save_jdat["profiles"][profile_id]["lifetime"]
    current = save_jdat["profiles"][profile_id]["current"]
    timing = save_jdat["profiles"][profile_id]["timing"]

    golden = ex1.GoldenModel(current["golden"])

    # Must do startup() to handle background accumulation.
    ex1.startup(timing, lifetime, current, buildings, upgrades, xupgrades)

    background_widget = BackgroundWidget()
    fps_widget = FPSWidget()
    x_widget = XWidget()
    donut_widget = TheDonut()
    buildings_widget = TheBuildings(buildings)
    upgrades_widget = TheUpgrades(upgrades, buildings, images)
    rollover_widget = RolloverWidget()
    golden_widget = GoldenWidget()
    stats_widget = StatsWidget()
    reset_widget = ResetWidget()

    font_set_idx = 0
    Fonts.activate_font_set(font_set_idx)

    running = True
    ticks = 0
    while running:
        ticks += 1

        if android:
            if android.check_pause():
                print "@@@@ pausing"
                # Save the game state to a file.
                with open(save_filenm, "w") as fp:
                    json.dump(save_jdat, fp, indent=4)
                android.wait_for_resume()
                print "@@@@ resuming"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                stats_widget.showing = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                background_widget._load_images()
                donut_widget._load_images()
                buildings_widget._load_images()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                font_set_idx = (font_set_idx + 1) % len(Fonts.font_sets)
                Fonts.activate_font_set(font_set_idx)

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
                elif golden_widget.on_click(event.pos):
                    pass
                elif donut_widget.on_click(event.pos):
                    # FINISH: put a function in ex1 to do this type of thing
                    current["cookies"] += current["cpc"]
                    current["game_cookies"] += current["cpc"]
                    lifetime["cookies"] += current["cpc"]
                elif buildings_widget.on_click(event.pos):
                    pass
                elif upgrades_widget.on_click(event.pos):
                    pass
                elif reset_widget.on_click(event.pos):
                    ex1.soft_reset(save_jdat["profiles"], profile_id, buildings, upgrades)
                    current = save_jdat["profiles"][profile_id]["current"]

            elif event.type == pygame.MOUSEMOTION:
                buildings_widget.on_mouseover(event.pos, rollover_widget)
                upgrades_widget.on_mouseover(event.pos, rollover_widget)

        # FINISH: make functions in ex1 which do all this work.
        # ex1.update_state(lifetime, current, elapsed)
        # ex1.calc_aux(lifetime, current) -> building_status, upgrade_status, golden_status?
        elapsed = ms_elapsed/1000.0
        ex1.update_state(elapsed, lifetime, current, buildings, upgrades, xupgrades)
        golden.update(elapsed)
        donut_widget.update(elapsed)
        stats_widget.update(current, lifetime)
        reset_widget.update(ex1.get_shard_value(save_jdat["profiles"], profile_id))

        building_costs = ex1.current_costs(current, buildings)

        # FINISH: make a XWidget.update() method.  Rename XWidget.
        x_widget.cps = current["cps"]
        x_widget.cpc = current["cpc"]
        x_widget.cookies = current["cookies"]
        x_widget.game_cookies = current["game_cookies"]

        buildings_widget.update(current, building_costs)
        upgrades_widget.update(current)
        golden_widget.update(golden)

        if MODE==2:
            #screen.fill(THECOLORS["black"])
            background_widget.draw(screen)
        else:
            background_widget.draw(screen)
        x_widget.draw(screen)
        buildings_widget.draw(screen)
        upgrades_widget.draw(screen)
        donut_widget.draw(screen)
        rollover_widget.draw(screen)
        fps_widget.draw(screen)

        golden_widget.draw(screen)
        stats_widget.draw(screen)
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


def main():
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        android.map_key(android.KEYCODE_BACK, pygame.K_q)

    GAMEDIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    if os.environ.get("PROFILE", "") == "1":
        import profile
        profile.run("main2()")
    else:
        sys.exit(main2())


if __name__ == '__main__':
    main()
