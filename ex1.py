import sys
import time
"""
lifetime
    cookies

current
    cookies
    cps
    buildings[building_id]
        base_cost
        base_cps
    upgrades[upgrade_id]
        cost
        target
        incr_pct
        incr_base_cps
        requirements[building_id] -> int

"""
COST_INCR = 1.15
PAUSE = 0.1


def setup():
    lifetime = {
        "cookies": 0.0
    }
    current = {
        "cookies": 0.0,
        "buildings": {
            "b1": 0,
            "b2": 0,
#           "b3": 0,
        },
        "upgrades": {
            "u1": False,
            "u2": False,
            "u3": False,
            "u4": False,
            "u5": False,
            "u6": False,
        }
    }
    buildings = {
        "b1": {"base_cost":10, "base_cps": 0.1, "name": "Glazed Donut", "description": "..."},
        "b2": {"base_cost":100, "base_cps": 0.7, "name": "Frosted Donut", "description": "Much more valuable than glaze, frosting originated in Donutavia."},
#       "b3": {"base_cost":150, "base_cps": 100.0},
    }
    upgrades = {
        "u1": {"cost": 100, "target": "b1", "incr_pct":2.0, "requirements": {"b1":1}, "name": "Extra Glaze"},
        "u2": {"cost": 1000, "target": "b1", "incr_pct":2.0, "requirements": {"b1":1}, "name": "Special Glaze"},
        "u3": {"cost": 10000, "target": "b1", "incr_pct":2.0, "requirements": {"b1":10}, "name": "Premium Glaze"},

        "u4": {"cost": 1000, "target": "b2", "incr_base_cps":1.3, "requirements": {"b2":1}, "name": "Extra Frosting"},
        "u5": {"cost": 10000, "target": "b2", "incr_pct":2.0, "requirements": {"b2":1}, "name": "Special Frosting"},
        "u6": {"cost": 100000, "target": "b2", "incr_pct":2.0, "requirements": {"b2":10}, "name": "Premium Frosting"},

    }
    # Invert the upgrade rules to be keyed by target.
    xupgrades = {}
    for upgrade_id, rule in upgrades.items():
        xupgrades.setdefault(rule["target"], [])
        xupgrades[rule["target"]].append(upgrade_id)
    return lifetime, current, buildings, upgrades, xupgrades


def current_costs(current, buildings):
    d = {}
    for building_id in buildings.keys():
        d[building_id] = (buildings[building_id]["base_cost"] *
            COST_INCR ** current["buildings"][building_id])
    return d


def get_buyable_buildings(current, buildings):
    s = set()
    building_costs = current_costs(current, buildings)
    for building_id in buildings.keys():
        cost = building_costs[building_id]
        if cost <= current["cookies"]:
            s.add(building_id)
    return s


def get_buyable_upgrades(current, upgrades):
    s = set()
    for upgrade_id in upgrades:
        cost = upgrades[upgrade_id]["cost"]
        if current["cookies"] >=  cost:
            s.add(upgrade_id)
    return s


def calc_cps(current, buildings, upgrades, xupgrades):
    # xupgrades[building_id] -> [upgrade_id, upgrade_id, ...]
    cps = 0.0
    for building_id in buildings.keys():
        base = buildings[building_id]["base_cps"]
        for upgrade_id in xupgrades.get(building_id, []):
            if current["upgrades"][upgrade_id]:
                base += upgrades[upgrade_id].get("incr_base_cps", 0.0)
        for upgrade_id in xupgrades.get(building_id, []):
            if current["upgrades"][upgrade_id]:
                base *= upgrades[upgrade_id].get("incr_pct", 1.0)
        base *= current["buildings"][building_id]
        cps += base
    # Special case for upgrades which don't apply to a specific building.
    building_id = "*"
    for upgrade_id in xupgrades.get(building_id, []):
        if current["upgrades"][upgrade_id]:
            cps += upgrades[upgrade_id].get("incr_base_cps", 0.0)
    for upgrade_id in xupgrades.get(building_id, []):
        if current["upgrades"][upgrade_id]:
            cps *= upgrades[upgrade_id].get("incr_pct", 1.0)
    return cps


def get_status(ticks, current):
    return "."
    return "%12s %10s %8s %6s %6s %6s %8s %8s %8s" % (
        ticks,
        "%.0f" % current["cookies"],
        int(current["cps"]),
        "b1=%s" % current["buildings"]["b1"],
        "b2=%s" % current["buildings"]["b2"],
        "b3=%s" % current["buildings"]["b3"],
        "u1=%s" % current["upgrades"]["u1"],
        "u2=%s" % current["upgrades"]["u2"],
        "u3=%s" % current["upgrades"]["u3"],
    )



def buy_building(current, buildings, building_id):
    building_costs = current_costs(current, buildings)
    cost = building_costs[building_id]
    if cost <= current["cookies"]:
        current["cookies"] -= cost
        current["buildings"][building_id] += 1
        return True
    return False


def get_building_text(current, buildings, building_id):
    name = buildings[building_id].get("name", building_id)
    descr = buildings[building_id].get("description", "...")
    dps = buildings[building_id]["base_cps"]
    return "%s -- Base DPS = %s -- %s" % (name, dps, descr)


def buy_upgrade(current, upgrades, upgrade_id):
    cost = upgrades[upgrade_id]["cost"]
    if cost > current["cookies"]:
        return False
    reqs = upgrades[upgrade_id]["requirements"]
    for building_id, cnt in reqs.items():
        if cnt > current["buildings"][building_id]:
            return False
    current["cookies"] -= cost
    current["upgrades"][upgrade_id] = True
    return True


def get_upgrade_text(current, upgrades, buildings, upgrade_id):
    name = upgrades[upgrade_id].get("name", upgrade_id)
    reqs = upgrades[upgrade_id]["requirements"]
    building_id, cnt = reqs.items()[0]
    descr = "Requires %s %s" % (cnt, buildings[building_id]["name"])
    if cnt > 1:
        descr += "s."
    else:
        descr += "."
    return "%s -- %d donuts -- %s" % (name, upgrades[upgrade_id]["cost"], descr)



def main():
    lifetime, current, buildings, upgrades, xupgrades = setup()

    ctrl = {
        5: "b1",
        10: "b1",
        20: "input",
    }

    ticks = 0
    for i in range(10000):
        ticks += 1

        if (ticks % 20) == 0:
            xid = raw_input("\n? ")
            if xid in current["buildings"]:
                current["buildings"][xid] += 1
            elif xid in current["upgrades"]:
                current["upgrades"][xid] = True

        cps = calc_cps(current, buildings, upgrades, xupgrades)
        current["cps"] = cps

        current["cookies"] = current["cookies"] + cps * PAUSE
        lifetime["cookies"] = lifetime["cookies"] + cps * PAUSE

        status = get_status(ticks, current)
        print >>sys.stderr, ("\r"+status),
        time.sleep(PAUSE)



if __name__=="__main__":
    main()


