import random

from common import *
import ex1 
from statswidget import StatsWidget

import pygame.transform




class XWidget:
    def __init__(self):
        self.cps = 0
        self.cpc = 1
        self.cookies = 0
        self.game_cookies = 0
        self._font = pygame.font.SysFont(None, 15)

    def draw(self, surface):
        cps_render = self._font.render("DPS: %s" % fmt(self.cps), True, TEXT_COLOR)
        cps_box = cps_render.get_rect()
        cps_box.left = 10
        cps_box.centery = 20
        surface.blit(cps_render, cps_box)

        cpc_render = self._font.render("DPC: %s" % fmt(self.cpc), True, TEXT_COLOR)
        cpc_box = cpc_render.get_rect()
        cpc_box.left = 10
        cpc_box.top = cps_box.bottom + 10
        surface.blit(cpc_render, cpc_box)

        cookies_render = self._font.render("Donuts: %s" % fmt(self.cookies), True, TEXT_COLOR)
        cookies_box = cookies_render.get_rect()
        cookies_box.left = 10
        cookies_box.top = cpc_box.bottom + 10
        surface.blit(cookies_render, cookies_box)
        
        game_cookies_render = self._font.render("Total Donuts: %s" % fmt(self.game_cookies), True, TEXT_COLOR)
        game_cookies_box = game_cookies_render.get_rect()
        game_cookies_box.left = 10
        game_cookies_box.top = cookies_box.bottom + 10
        surface.blit(game_cookies_render, game_cookies_box)



class TheDonut:
    def __init__(self):
        image_file = DONUT_IMAGE
        self.img = pygame.image.load(os.path.join(GAMEDIR, image_file))
        self.img = pygame.transform.smoothscale(self.img, (256, 256))
        self.box = self.img.get_rect()
        self.box.center = (SCREEN_WIDTH/6, SCREEN_HEIGHT/2)

    def update(self):
        pass

    def on_click(self, pos):
        pass

    def draw(self, surface):
        surface.blit(self.img, self.box)


class TheBuildings:
    def __init__(self, buildings):
        self.buildings = buildings
        self._font = pygame.font.SysFont(None, 15)
        self.boxes = []

    def update(self, current, building_costs):
        self.current = current
        self.building_costs = building_costs

    def draw(self, surface):
        y = 20
        self.boxes = []
        buyable = ex1.get_buyable_buildings(self.current, self.buildings)
        for building_id in sorted(self.buildings.keys()):
            if building_id in buyable:
                color = TEXT_COLOR
            else:
                color = THECOLORS["orange"]
            name = self.buildings[building_id].get("name", building_id)
            render = self._font.render("%s (%d) -- Cost: %s" % (name,
                self.current["buildings"][building_id],
                fmt(self.building_costs[building_id])),
                True, color)
            box = render.get_rect()
            box.left = 1.4 * SCREEN_WIDTH / 5
            box.centery = y
            surface.blit(render, box)
            y += box.height + 10

            self.boxes.append(box)

    def on_click(self, pos):
        building_ids = sorted(self.buildings.keys())
        for box, building_id in zip(self.boxes, building_ids):
            if box.collidepoint(pos):
                ex1.buy_building(self.current, self.buildings, building_id)

    def on_mouseover(self, pos, rollover_widget):
        building_ids = sorted(self.buildings.keys())
        for box, building_id in zip(self.boxes, building_ids):
            if box.collidepoint(pos):
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
        self.available_img = pygame.image.load(os.path.join(GAMEDIR, image_file))
        self.available_img = pygame.transform.smoothscale(self.available_img, (40, 40))
        self.available_box = self.available_img.get_rect()
        self.available_box.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        image_file = GOLDEN_ACTIVE_IMAGE
        self.active_img = pygame.image.load(os.path.join(GAMEDIR, image_file))
        self.active_img = pygame.transform.smoothscale(self.active_img, (40, 40))
        self.active_box = self.active_img.get_rect()
        self.active_box.center = (SCREEN_WIDTH/6, 4*SCREEN_HEIGHT/5)
        self.last_state = ("", False)  # state, active

        self._font = pygame.font.SysFont(None, 15)


    def update(self, golden):
        self.golden = golden
        if self.last_state == (self.golden.data["state"], self.golden.data["active"]):
            return
        # Track the last state for the next call.
        self.last_state = (golden.data["state"], golden.data["active"])
        # There was a state transition, so pick a new random location for next golden.
        self.x = random.randrange(SCREEN_WIDTH)
        self.y = random.randrange(SCREEN_HEIGHT)
        self.available_box.center = (self.x, self.y)
        if self.golden.data["state"] == "waiting":
            # Draw will do nothing during waiting state.
            self.draw = lambda x:None
        elif self.golden.data["state"] == "available" and not self.golden.data["active"]:
            self.draw = self._draw_avail
        elif self.golden.data["state"] == "available" and self.golden.data["active"]:
            self.draw = self._draw_active
            # Prep the text for the current golden.
            rule = self.golden.get_ctrl()
            self.text_render = self._font.render("%s" % (rule["name"],), True, (0,255,0))
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
 


class TheUpgrades:
    def __init__(self, upgrades, buildings, images):
        self.upgrades = upgrades
        self.buildings = buildings
        self.images = images
        self._font = pygame.font.SysFont(None, 30)
        self.boxes = []

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
        for idx, upgrade_id in enumerate(sorted(self.upgrades.keys())):
            row = (idx // per_row)
            col = (idx % per_row)

            if self.current["upgrades"][upgrade_id]:
                img = self.images.imgs[1]
            elif upgrade_id in buyable:
                img = self.images.imgs[0]
            elif upgrade_id in buyable2:
                img = self.images.imgs[3]
            else:
                img = self.images.imgs[2]

            box = img.get_rect()
            box.left = init_left + col * box.width
            box.centery = init_centery + row * box.height

            surface.blit(img, box)
            self.boxes.append(box)


    def on_click(self, pos):
        upgrade_ids = sorted(self.upgrades.keys())
        for box, upgrade_id in zip(self.boxes, upgrade_ids):
            if box.collidepoint(pos):
                ex1.buy_upgrade(self.current, self.upgrades, upgrade_id)

    def on_mouseover(self, pos, rollover_widget):
        upgrade_ids = sorted(self.upgrades.keys())
        for box, upgrade_id in zip(self.boxes, upgrade_ids):
            if box.collidepoint(pos):
                text = ex1.get_upgrade_text(self.current, self.upgrades, self.buildings, upgrade_id)
                rollover_widget.update(text)



class RolloverWidget:
    def __init__(self):
        self._font = pygame.font.SysFont(None, 15)
        self.line1 = "."
        self.line2 = "."
        self.update("\n")

    def update(self, text):
        line1, line2 = text.split("\n", 1)
        if line1 == self.line1 and line2 == self.line2:
            return

        self.line1 = line1
        self.line2 = line2

        self.line2_render = self._font.render(self.line2, True, (155,155,155))
        self.line2_box = self.line2_render.get_rect()
        self.line2_box.bottom = SCREEN_HEIGHT - 10
        self.line2_box.centerx = SCREEN_WIDTH / 2

        self.line1_render = self._font.render(self.line1, True, TEXT_COLOR)
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
            img = pygame.image.load(image_file)
            self.imgs.append(img)


class BackgroundWidget:
    def __init__(self):
        img = pygame.image.load(os.path.join(GAMEDIR, BACKGROUND_IMAGE))
        self.img = pygame.transform.smoothscale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.box = self.img.get_rect()
        self.box.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)


    def draw(self, surface):
        surface.blit(self.img, self.box)




def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DISPLAY_FLAGS)
    app_name = "Rockwell's Uninformed Tidemark"
    pygame.display.set_caption(app_name)

    clock = pygame.time.Clock()

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
    x_widget = XWidget()
    donut_widget = TheDonut()
    buildings_widget = TheBuildings(buildings)
    upgrades_widget = TheUpgrades(upgrades, buildings, images)
    rollover_widget = RolloverWidget()
    golden_widget = GoldenWidget()

    running = True
    ticks = 0
    while running:
        ticks += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
                # FINISH: put a function in ex1 to do this type of thing
                if donut_widget.box.collidepoint(event.pos):
                    current["cookies"] += current["cpc"]
                    current["game_cookies"] += current["cpc"]
                    lifetime["cookies"] += current["cpc"]
                else:
                    buildings_widget.on_click(event.pos)
                    upgrades_widget.on_click(event.pos)
                    golden_widget.on_click(event.pos)

            elif event.type == pygame.MOUSEMOTION:
                buildings_widget.on_mouseover(event.pos, rollover_widget)
                upgrades_widget.on_mouseover(event.pos, rollover_widget)

        # FINISH: make functions in ex1 which do all this work.
        # ex1.update_state(lifetime, current, elapsed)
        # ex1.calc_aux(lifetime, current) -> building_status, upgrade_status, golden_status?
#       cps, cpc = ex1.calc_cps(current, buildings, upgrades, xupgrades)
#       current["cps"] = cps
#       current["cpc"] = cpc
#       current["cookies"] += cps * 1 / float(TICK)
#       current["game_cookies"] += cps * 1 / float(TICK)
#       lifetime["cookies"] += cps * 1 / float(TICK)
        elapsed = 1 / float(TICK)
        ex1.update_state(elapsed, lifetime, current, buildings, upgrades, xupgrades)
        golden.update(elapsed)

        building_costs = ex1.current_costs(current, buildings)
#       status = ex1.get_status(ticks, current)
#       print >>sys.stderr, ("\r"+status),

        # FINISH: make a XWidget.update() method.  Rename XWidget.
        x_widget.cps = current["cps"]
        x_widget.cpc = current["cpc"]
        x_widget.cookies = current["cookies"]
        x_widget.game_cookies = current["game_cookies"]

        buildings_widget.update(current, building_costs)
        upgrades_widget.update(current)
        golden_widget.update(golden)

        screen.fill(THECOLORS["blue"])

        background_widget.draw(screen)
        x_widget.draw(screen)
        buildings_widget.draw(screen)
        upgrades_widget.draw(screen)
        donut_widget.draw(screen)
        rollover_widget.draw(screen)

        golden_widget.draw(screen)

        pygame.display.flip()
        ms_elapsed = clock.tick(TICK)

#       timer.update((ms_elapsed/1000.0)*TICK) # FINISH: does flip() returns the elapsed ti
#       finish_timer.update((ms_elapsed/1000.0)*TICK) # FINISH: does flip() returns the ela
        pygame.event.pump()

    # Must do shutdown() to prep for background accumulation.
    ex1.shutdown(timing)

    # Save the game state to a file.
    with open(save_filenm, "w") as fp:
        json.dump(save_jdat, fp, indent=4)


if __name__ == '__main__':
    GAMEDIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    sys.exit(main())
