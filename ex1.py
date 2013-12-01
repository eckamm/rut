import sys
import os
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


def init_savegame(filenm):
    """
    Create an empty save game file.
    """
    jdat = {
        "profiles": [
            {"name": "D"},
            {"name": "O"},
            {"name": "N"},
            {"name": "U"},
            {"name": "T"},
        ]
    }
    with open(filenm, "w") as fp:
        json.dump(jdat, fp, indent=4)


def sync_rules(save_filenm, buildings, upgrades):
    """
    Re-write the save data to be in sync with the rules.
    """
    # Get the current save data.
    with open(save_filenm, "r") as fp:
        jdat = json.load(fp)
    # Sync each profile to current rules.
    for p in jdat["profiles"]:
        # Replace the lifetime save state.
        tmp = {}
        tmp["cookies"] = p.get("lifetime", {}).get("cookies", 0.0)
        p["lifetime"] = tmp
        # Replace the current save state.
        tmp = {}
        tmp["cookies"] = p.get("current", {}).get("cookies", 0.0)
        tmp["game_cookies"] = p.get("current", {}).get("game_cookies", 0.0)
        tmp["cpc"] = p.get("current", {}).get("cpc", 1.0)
        # Replace the current->buildings save state.
        tmp["buildings"] = {}
        for building_id in buildings:
            tmp["buildings"][building_id] = p.get("current", {}).get("buildings", {}).get(building_id, 0)
        # Replace the current->upgrades save state.
        tmp["upgrades"] = {}
        for upgrade_id in upgrades:
            tmp["upgrades"][upgrade_id] = p.get("current", {}).get("upgrades", {}).get(upgrade_id, False)
        p["current"] = tmp
    # Write out the synced save data.
    with open(save_filenm, "w") as fp:
        json.dump(jdat, fp, indent=4)



def setup(save_filenm, rules_filenm):
    """
    returns (save_jdat, buildings, upgrades, xupgrades)
    """

    # Make an empty save profiles file.
    if not os.path.exists(save_filenm):
        init_savegame(save_filenm)

    # Load the rules.
    with open(rules_filenm) as fp:
        rules_jdat = json.load(fp)
    buildings = rules_jdat["buildings"]
    upgrades = rules_jdat["upgrades"]

    # Load the save data.
    with open(save_filenm) as fp:
        save_jdat = json.load(fp)
    # Sync the save data to match the current rules.
    sync_rules(save_filenm, buildings, upgrades)
    # Load the save data.
    with open(save_filenm) as fp:
        save_jdat = json.load(fp)

    # Invert the upgrade rules to be keyed by target.
    xupgrades = {}
    for upgrade_id, rule in upgrades.items():
        xupgrades.setdefault(rule["target"], [])
        xupgrades[rule["target"]].append(upgrade_id)

    profile_id = 0
    lifetime = save_jdat["profiles"][profile_id]["lifetime"]
    current = save_jdat["profiles"][profile_id]["current"]

    return save_jdat, buildings, upgrades, xupgrades


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
        reqs = upgrades[upgrade_id]["requirements"]
        cost = upgrades[upgrade_id]["cost"]
        x = True
        for building_id, cnt in reqs.items():
            if building_id == "game_cookies":
                if cnt > current["cookies"]:
                    x = False
            elif cnt > current["buildings"][building_id]:
                x = False
                break
        if current["cookies"] >=  cost and x:
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
    # Special case for increasing cpc: Rename function to something else!
    building_id = "click"
    cpc = 1.0
    for upgrade_id in xupgrades.get(building_id, []):
        if current["upgrades"][upgrade_id]:
            cpc += upgrades[upgrade_id].get("incr_base_cps", 0.0)
    for upgrade_id in xupgrades.get(building_id, []):
        if current["upgrades"][upgrade_id]:
            cpc *= upgrades[upgrade_id].get("incr_pct", 1.0)
    return cps, cpc


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
    if upgrade_id in get_buyable_upgrades(current, upgrades):
        cost = upgrades[upgrade_id]["cost"]
        current["cookies"] -= cost
        current["upgrades"][upgrade_id] = True
    return True


def get_upgrade_text(current, upgrades, buildings, upgrade_id):
    name = upgrades[upgrade_id].get("name", upgrade_id)
    reqs = upgrades[upgrade_id]["requirements"]
    building_id, cnt = reqs.items()[0]
    if building_id == "game_cookies":
        descr = "Requires %s game cookie" % (cnt)
    else:
        descr = "Requires %s %s" % (cnt, buildings[building_id]["name"])
    flavor = upgrades[upgrade_id].get("flavor", "...")
    building_id = upgrades[upgrade_id]["target"]
    if upgrades[upgrade_id].get("incr_pct", "") != "":
        if building_id == "click":
            descr2 = "Multiplies click by %s" % (upgrades[upgrade_id]["incr_pct"])
        else:
            descr2 = "Multiplies %s's output by %s." % (buildings[building_id]["name"], upgrades[upgrade_id]["incr_pct"])
    if upgrades[upgrade_id].get("incr_base_cps", "") != "":
        if building_id == "click":
            descr2 = "Adds to click by %s" % (upgrades[upgrade_id]["incr_base_cps"])
        else:
            descr2 = "Adds %s to %s's base cps." % (upgrades[upgrade_id]["incr_base_cps"], buildings[building_id]["name"])
    
    if cnt > 1:
        descr += "s."
    else:
        descr += "."
    return "%s -- %d donuts -- %s -- %s\n%s" % (name, upgrades[upgrade_id]["cost"], descr, descr2,flavor)



def main():
    save_jdat, buildings, upgrades, xupgrades = setup("savegame.json", "params.json")
    profile_id = 0
    lifetime = save_jdat["profiles"][profile_id]["lifetime"]
    current = save_jdat["profiles"][profile_id]["current"]

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

        cps, cpc = calc_cps(current, buildings, upgrades, xupgrades)
        current["cps"] = cps
        current["cpc"] = cpc

        current["cookies"] = current["cookies"] + cps * PAUSE
        lifetime["cookies"] = lifetime["cookies"] + cps * PAUSE

        status = get_status(ticks, current)
        print >>sys.stderr, ("\r"+status),
        time.sleep(PAUSE)



if __name__=="__main__":
    main()


