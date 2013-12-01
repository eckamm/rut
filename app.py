from common import *



class XWidget:
    def __init__(self):
        self.cps = 0
        self.cookies = 0
        self.game_cookies = 0
        self._font = pygame.font.SysFont(None, 30)

    def draw(self, surface):
        cps_render = self._font.render("DPS: %.1f" % self.cps, True, (255,255,255))
        cps_box = cps_render.get_rect()
        cps_box.left = 10
        cps_box.centery = 20
        surface.blit(cps_render, cps_box)

        cookies_render = self._font.render("Donuts: %d" % self.cookies, True, (255,255,255))
        cookies_box = cookies_render.get_rect()
        cookies_box.left = 10
        cookies_box.top = cps_box.bottom + 10
        surface.blit(cookies_render, cookies_box)
        
        game_cookies_render = self._font.render("Game Donuts: %d" % self.game_cookies, True, (255,255,255))
        game_cookies_box = game_cookies_render.get_rect()
        game_cookies_box.left = 10
        game_cookies_box.top = cookies_box.bottom + 10
        surface.blit(game_cookies_render, game_cookies_box)


class TheDonut:
    def __init__(self):
        image_file = "donut.png"
        self.img = pygame.image.load(os.path.join(GAMEDIR, image_file))
        self.box = self.img.get_rect()
        self.box.center = (SCREEN_WIDTH/5, SCREEN_HEIGHT/2)

    def draw(self, surface):
        surface.blit(self.img, self.box)


class TheBuildings:
    def __init__(self, buildings):
        self.buildings = buildings
        self._font = pygame.font.SysFont(None, 30)
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
                color = THECOLORS["white"]
            else:
                color = THECOLORS["orange"]
            render = self._font.render("%s: %d  %d" % (building_id,
                self.building_costs[building_id],
                self.current["buildings"][building_id]),
                True, color)
            box = render.get_rect()
            box.left = 2 * SCREEN_WIDTH / 5
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



class TheUpgrades:
    def __init__(self, upgrades, buildings):
        self.upgrades = upgrades
        self.buildings = buildings
        self._font = pygame.font.SysFont(None, 30)
        self.boxes = []

    def update(self, current):
        self.current = current

    def draw(self, surface):
        y = 20
        self.boxes = []
        buyable = ex1.get_buyable_upgrades(self.current, self.upgrades)
        for upgrade_id in sorted(self.upgrades.keys()):
            if self.current["upgrades"][upgrade_id]:
                color = THECOLORS["green"]
            elif upgrade_id in buyable:
                color = THECOLORS["white"]
            else:
                color = THECOLORS["orange"]
            render = self._font.render("%s: %s" % (upgrade_id,
                self.current["upgrades"][upgrade_id]),
                True, color)
            box = render.get_rect()
            box.left = 4 * SCREEN_WIDTH / 5
            box.centery = y
            surface.blit(render, box)
            y += box.height + 10

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
        self._font = pygame.font.SysFont(None, 20)
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

        self.line1_render = self._font.render(self.line1, True, (255,255,255))
        self.line1_box = self.line1_render.get_rect()
        self.line1_box.bottom = self.line2_box.top - 10
        self.line1_box.centerx = SCREEN_WIDTH / 2



    def draw(self, surface):
        surface.blit(self.line1_render, self.line1_box)
        surface.blit(self.line2_render, self.line2_box)



def main():
    pygame.init()
#   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    app_name = "Rockwell's Uninformed Tidemark"
    pygame.display.set_caption(app_name)

    clock = pygame.time.Clock()

    rules_filenm = os.path.join(GAMEDIR, "params.json")
    save_filenm = os.path.join(GAMEDIR, "savegame.json")
    save_jdat, buildings, upgrades, xupgrades = ex1.setup("savegame.json", "params.json")
    profile_id = 0
    lifetime = save_jdat["profiles"][profile_id]["lifetime"]
    current = save_jdat["profiles"][profile_id]["current"]

    x_widget = XWidget()
    donut_widget = TheDonut()
    buildings_widget = TheBuildings(buildings)
    upgrades_widget = TheUpgrades(upgrades, buildings)
    rollover_widget = RolloverWidget()

    running = True
    ticks = 0
    while running:
        ticks += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open(save_filenm, "w") as fp:
                    json.dump(save_jdat, fp, indent=4)
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                current["cookies"] += 100000
                current["game_cookies"] += 100000
                lifetime["cookies"] += 100000

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFTBUTTON:
                if donut_widget.box.collidepoint(event.pos):
                    current["cookies"] += current["cpc"]
                    current["game_cookies"] += current["cpc"]
                    lifetime["cookies"] += current["cpc"]
                else:
                    buildings_widget.on_click(event.pos)
                    upgrades_widget.on_click(event.pos)

            elif event.type == pygame.MOUSEMOTION:
                buildings_widget.on_mouseover(event.pos, rollover_widget)
                upgrades_widget.on_mouseover(event.pos, rollover_widget)


        cps, cpc = ex1.calc_cps(current, buildings, upgrades, xupgrades)
        current["cps"] = cps
        current["cpc"] = cpc
        current["cookies"] = current["cookies"] + cps * 1 / float(TICK)
        current["game_cookies"] += cps * 1 / float(TICK)
        lifetime["cookies"] += cps * 1 / float(TICK)
        status = ex1.get_status(ticks, current)
        building_costs = ex1.current_costs(current, buildings)
        print >>sys.stderr, ("\r"+status),


        screen.fill(THECOLORS["blue"])

        x_widget.cps = current["cps"]
        x_widget.cookies = current["cookies"]
        x_widget.game_cookies = current["game_cookies"]

        buildings_widget.update(current, building_costs)
        upgrades_widget.update(current)

        x_widget.draw(screen)
        buildings_widget.draw(screen)
        upgrades_widget.draw(screen)
        donut_widget.draw(screen)
        rollover_widget.draw(screen)

        pygame.display.flip()
        ms_elapsed = clock.tick(TICK)

#       timer.update((ms_elapsed/1000.0)*TICK) # FINISH: does flip() returns the elapsed ti
#       finish_timer.update((ms_elapsed/1000.0)*TICK) # FINISH: does flip() returns the ela
        pygame.event.pump()



if __name__ == '__main__':
    GAMEDIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    sys.exit(main())
