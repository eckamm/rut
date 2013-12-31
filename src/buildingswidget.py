import os

from common import *
from fonts import Fonts
import ex1 


class BuildingsWidget:
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
        y = 5
        self.boxes = []
        buyable = ex1.get_buyable_buildings(self.current, self.buildings)
        for idx, building_id in enumerate(sorted(self.buildings.keys())):
            if building_id in buyable:
                color = TEXT_COLOR
            else:
                color = THECOLORS["orange"]
            name = self.buildings[building_id].get("name", building_id)
            render = make_text(Fonts.f15, "%s (%d)" % (name,
                self.current["buildings"][building_id]),
                TEXT_ANTIALIAS, color, TEXT_BACKGROUND)
            render2 = make_text(Fonts.f12, "Cost: %s" % (
                fmt(self.building_costs[building_id])),
                TEXT_ANTIALIAS, color, TEXT_BACKGROUND)

            box2 = self.images[idx].get_rect()
            box2.top = y
            if MODE == 2:
                box2.left = 0
            else:
                box2.left = 1.4 * SCREEN_WIDTH / 5
            surface.blit(self.images[idx], box2)

            box = render.get_rect()
            box.left = box2.right + 2
            box.bottom = box2.centery
            surface.blit(render, box)

            box3 = render2.get_rect()
            box3.left = box2.right + 2
            box3.top = box2.centery
            surface.blit(render2, box3)

            y += box2.height + 5
            self.boxes.append((box, box2, box3))

    def on_click(self, pos):
        building_ids = sorted(self.buildings.keys())
        for boxes, building_id in zip(self.boxes, building_ids):
            for box in boxes:
                if box.collidepoint(pos):
                    ex1.buy_building(self.current, self.buildings, building_id)
                    return True

    def on_mouseover(self, pos, rollover_widget):
        building_ids = sorted(self.buildings.keys())
        for boxes, building_id in zip(self.boxes, building_ids):
            for box in boxes:
                if box.collidepoint(pos):
                    text = ex1.get_building_text(self.current, self.buildings, building_id)
                    rollover_widget.update(text)



class BuildingsWidget:
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
        y = 5
        self.boxes = []
        buyable = ex1.get_buyable_buildings(self.current, self.buildings)
        for idx, building_id in enumerate(sorted(self.buildings.keys())):
            if building_id in buyable:
                color = TEXT_COLOR
            else:
                color = THECOLORS["orange"]
            name = self.buildings[building_id].get("name", building_id)
            render = make_text(Fonts.f18, "%s (%d)" % (name,
                self.current["buildings"][building_id]),
                TEXT_ANTIALIAS, color, TEXT_BACKGROUND)
            render2 = make_text(Fonts.f18, "Cost: %s" % (
                fmt(self.building_costs[building_id])),
                TEXT_ANTIALIAS, color, TEXT_BACKGROUND)

            box2 = self.images[idx].get_rect()
            box2.top = y
            if MODE == 2:
                box2.left = 0
            else:
                box2.left = 1.4 * SCREEN_WIDTH / 5
            surface.blit(self.images[idx], box2)

            box = render.get_rect()
            box.left = box2.right + 2
            box.bottom = box2.centery
            surface.blit(render, box)

            box3 = render2.get_rect()
            box3.left = box2.right + 2
            box3.top = box2.centery
            surface.blit(render2, box3)

            y += box2.height + 5
            self.boxes.append((box, box2, box3))

    def on_click(self, pos):
        building_ids = sorted(self.buildings.keys())
        for boxes, building_id in zip(self.boxes, building_ids):
            for box in boxes:
                if box.collidepoint(pos):
                    ex1.buy_building(self.current, self.buildings, building_id)
                    return True

    def on_mouseover(self, pos, rollover_widget):
        building_ids = sorted(self.buildings.keys())
        for boxes, building_id in zip(self.boxes, building_ids):
            for box in boxes:
                if box.collidepoint(pos):
                    text = ex1.get_building_text(self.current, self.buildings, building_id)
                    rollover_widget.update(text)



