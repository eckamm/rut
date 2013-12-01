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
            "b3": 0,
        },
        "upgrades": {
            "u1": False,
            "u2": False,
            "u3": False
        }
    }
    buildings = {
        "b1": {"base_cost":5, "base_cps": 5.0},
        "b2": {"base_cost":50, "base_cps": 50.0},
        "b3": {"base_cost":150, "base_cps": 100.0},
    }
    upgrades = {
        "u1": {"cost": 100, "target": "b1", "incr_pct":1.05},
        "u2": {"cost": 1000, "target": "b1", "incr_base_cps": 1000},
        "u3": {"cost": 10000, "target": "*", "incr_pct":1.05},
    }
    # Invert the upgrade rules to be keyed by target.
    xupgrades = {}
    for upgrade_id, rule in upgrades.items():
        xupgrades.setdefault(rule["target"], [])
        xupgrades[rule["target"]].append(upgrade_id)
    return lifetime, current, buildings, upgrades, xupgrades


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


