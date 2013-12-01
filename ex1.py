import sys
import time
import json
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


def setup(filenm):

    with open(filenm) as fp:
        jdat = json.load(fp)

    lifetime = {
        "cookies": 0.0
    }
    current = {
        "cookies": 0.0,
        "buildings": {
        },
        "upgrades": {
        }
    }

    buildings = jdat["buildings"]
    upgrades = jdat["upgrades"]

    # Prime the current state.
    for building_id in buildings:
        current["buildings"][building_id] = 0
    for upgrade_id in upgrades:
        current["upgrades"][upgrade_id] = False

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
        d[building_id] = long(d[building_id])
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
    return "%s -- Base DPS = %s\n%s" % (name, dps, descr)


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
    flavor = upgrades[upgrade_id].get("flavor", "...")
    if cnt > 1:
        descr += "s."
    else:
        descr += "."
    return "%s -- %d donuts -- %s\n%s" % (name, upgrades[upgrade_id]["cost"], descr,flavor)



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


