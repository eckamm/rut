import sys
import os
import time
import json
import random
import math

from common import fmt
"""
profiles[]

    timing
        start_ts -> float; set in startup() and shutdown()
        stop_ts -> float; set in startup() and shutdown()
        bg_seconds -> float; set by startup()
        fg_seconds -> float; set by shutdown()

    lifetime
        cookies -> float (earned ever)
        bg_cookies -> float
        shards -> int (always round down)

    current
        cookies -> float (currently owned)
        game_cookies -> float (earned in current game)
        cps -> float? (updated by update_state())
        cpc -> float? (updated by update_state())
        buildings[building_id] -> int
        upgrades[upgrade_id] -> bool

        golden
            state -> string; waiting|available
            timer -> float; counts down to next state transition
            active -> bool; if active when state is available then apply effect
            kind -> string; a key from GoldenModel.rules



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


class GoldenModel:
    """
    state -> string; waiting|available
    timer -> float; counts down to next state transition
    active -> bool; if active when state is available then apply effect
    kind -> string; a key from GoldenModel.rules

    timeline of a golden cookie

    ------+++++++------++++/////-------
    1     2      1     2   3    1

    1 -> state=waiting   active=False
    2 -> state=available active=False
    3 -> state=available active=True

    - -> time spent waiting for a golden cookie
    + -> time wasted not clicking on an available golden
    / -> time golden cookie effects are in effect

    ["cps", 2.0] -> multiple CPS by two
    ["cpc", 2.0] -> multiple CPC by two
    ["cookies", 2.0] -> add 2*current["cookies"]
    """
    rules = {
        "gr10": {"name": "Frenzy", "weight": 10, "effects": [["cps", 2.0], ["cpc", 2.0]]},
        "gr20": {"name": "Super-frenzy", "weight": 5, "effects": [["cps", 8.0], ["cpc", 8.0]]},
    }

    def __init__(self, data):
        # data is a reference to savegame["profiles"][profile_id]["golden"]
        self.data = data

    def update(self, elapsed):
        d = self.data
        d["timer"] -= elapsed
        if d["state"] == "waiting":
            if d["timer"] <= 0.0:
                # transition from waiting to available
                d["state"] = "available"
                d["timer"] = float(random.randrange(3, 6))
                pot = []
                for rule_id in self.rules:
                    pot.extend([rule_id]*self.rules[rule_id]["weight"])
                d["kind"] = random.choice(pot)
                print >>sys.stderr, "golden transitioned to available; kind=%s; timer=%.1f" % (d["kind"], d["timer"])
        elif d["state"] == "available":
            if d["timer"] <= 0.0:
                # transition from available to waiting
                d["state"] = "waiting"
                d["timer"] = float(random.randrange(3, 20))
                d["active"] = False
                print >>sys.stderr, "golden transitioned to waiting; timer=%.1f" % (d["timer"],)
        else:
            pass

    def activate(self):
        d = self.data
        if d["state"] == "available":
            d["active"] = True

    def get_ctrl(self):
        d = self.data
        if d["active"]:
            return d["kind"], self.rules[d["kind"]]
        return None




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
        # Replace the "timing" save state data.
        tmp = {}
        tmp["start_ts"] = p.get("timing", {}).get("start_ts", 0.0)
        tmp["stop_ts"] = p.get("timing", {}).get("stop_ts", 0.0)
        tmp["bg_seconds"] = p.get("timing", {}).get("bg_seconds", 0.0)
        tmp["fg_seconds"] = p.get("timing", {}).get("fg_seconds", 0.0)
        p["timing"] = tmp
        # Replace the "lifetime" save state data.
        tmp = {}
        tmp["cookies"] = p.get("lifetime", {}).get("cookies", 0.0)
        tmp["bg_cookies"] = p.get("lifetime", {}).get("bg_cookies", 0.0)
        tmp["shards"] = p.get("lifetime", {}).get("shards", 0)
        p["lifetime"] = tmp
        # Replace the "current" save state data.
        p["current"] = mk_new_current(buildings, upgrades, src=p.get("current", {}))
#       tmp = {}
#       tmp["cookies"] = p.get("current", {}).get("cookies", 0.0)
#       tmp["game_cookies"] = p.get("current", {}).get("game_cookies", 0.0)
#       tmp["cpc"] = p.get("current", {}).get("cpc", 1.0)
#       # Replace the current->buildings save state.
#       tmp["buildings"] = {}
#       for building_id in buildings:
#           tmp["buildings"][building_id] = p.get("current", {}).get("buildings", {}).get(building_id, 0)
#       # Replace the current->upgrades save state.
#       tmp["upgrades"] = {}
#       for upgrade_id in upgrades:
#           tmp["upgrades"][upgrade_id] = p.get("current", {}).get("upgrades", {}).get(upgrade_id, False)
#       p["current"] = tmp
    # Write out the synced save data.
    with open(save_filenm, "w") as fp:
        json.dump(jdat, fp, indent=4)


def mk_new_current(buildings, upgrades, src={}):
    """
    create new "current" optionally copying in data from src
    """
    current = {}
    current["cookies"] = src.get("cookies", 0.0)
    current["game_cookies"] = src.get("game_cookies", 0.0)
    current["cpc"] = src.get("cpc", 1.0)
    current["cps"] = src.get("cps", 0.0)
    current["buildings"] = {}
    for building_id in buildings:
        current["buildings"][building_id] = src.get("buildings", {}).get(building_id, 0)
    current["upgrades"] = {}
    for upgrade_id in upgrades:
        current["upgrades"][upgrade_id] = src.get("upgrades", {}).get(upgrade_id, False)
    current["golden"] = {}
    current["golden"]["state"] = src.get("golden", {}).get("state", "waiting")
    current["golden"]["timer"] = src.get("golden", {}).get("timer", 1.0)
    current["golden"]["active"] = src.get("golden", {}).get("active", False)
    current["golden"]["kind"] = src.get("golden", {}).get("kind", "")
    return current



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


def get_buyable_upgrades(current, upgrades, can_buy = True):
    s = set()
    for upgrade_id in upgrades:
        reqs = upgrades[upgrade_id]["requirements"]
        cost = upgrades[upgrade_id]["cost"]
        x = True
        for building_id, cnt in reqs.items():
            if building_id == "game_cookies":
                if cnt > current["game_cookies"]:
                    x = False
            elif cnt > current["buildings"][building_id]:
                x = False
                break
        if can_buy:
            if current["cookies"] >=  cost and x:
                s.add(upgrade_id)
        else:
            if x:
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
    multcpc = 1
    for upgrade_id in xupgrades.get(building_id, []):
        if current["upgrades"][upgrade_id]:
            cps += upgrades[upgrade_id].get("incr_base_cps", 0.0)
    for upgrade_id in xupgrades.get(building_id, []):
        if current["upgrades"][upgrade_id]:
            cps *= upgrades[upgrade_id].get("incr_pct", 1.0)
            multcpc *= upgrades[upgrade_id].get("incr_pct", 1.0)
    # Special case for increasing cpc: Rename function to something else!
    building_id = "click"
    cpc = 1.0
    for upgrade_id in xupgrades.get(building_id, []):
        if current["upgrades"][upgrade_id]:
            cpc += upgrades[upgrade_id].get("incr_base_cps", 0.0)
    for upgrade_id in xupgrades.get(building_id, []):
        if current["upgrades"][upgrade_id]:
            cpc *= upgrades[upgrade_id].get("incr_pct", 1.0)
    cpc *= multcpc

    golden = GoldenModel(current["golden"])
    ctrl = golden.get_ctrl()
    if ctrl is None:
        gfactor = 1.0
    else:
        gfactor = 2.0
    cps = cps * gfactor

    return cps, cpc


def update_state(elapsed, lifetime, current, buildings, upgrades, xupgrades, bg=False):
    """
    elapsed is time in seconds since last update; e.g. 1/float(TICK)
    """
    sfactor = 1 + (lifetime["shards"]/50.0)
    cps, cpc = calc_cps(current, buildings, upgrades, xupgrades)
    cps *= sfactor
    cpc *= sfactor
    current["cps"] = cps
    current["cpc"] = cpc
    current["cookies"] += cps * elapsed
    current["game_cookies"] += cps * elapsed
    lifetime["cookies"] += cps * elapsed
    if bg is True:
        lifetime["bg_cookies"] += cps * elapsed


def startup(timing, lifetime, current, buildings, upgrades, xupgrades):
    """
    call this to start a game session
    """
    now = time.time()
    if timing["stop_ts"] != 0.0:
        bg_elapsed = now - timing["stop_ts"]
        timing["bg_seconds"] += bg_elapsed
        prev_cookies = current["cookies"]
        slimdown_factor = 0.1
        update_state(slimdown_factor*bg_elapsed, lifetime, current, buildings, upgrades, xupgrades, bg=True)
        print >>sys.stderr, "handled %.1f bg_seconds; gained %.1f donuts" % (bg_elapsed, current["cookies"]-prev_cookies)
    timing["start_ts"] = now
    timing["stop_ts"] = 0.0


def shutdown(timing):
    """
    call this to end a game session
    """
    now = time.time()
    fg_elapsed = now - timing["start_ts"]
    timing["start_ts"] = 0.0
    print >>sys.stderr, "handled %.1f fg_seconds" % fg_elapsed
    timing["fg_seconds"] += fg_elapsed
    timing["stop_ts"] = now



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



def soft_reset(profiles, profile_id, buildings, upgrades):
    """
    do a "soft reset"

    A soft reset establishes how many shards you have and resets
    the current game session.
    """
    # FINISH: need formula
    profiles[profile_id]["lifetime"]["shards"] = int((math.sqrt(1+(8*(profiles[profile_id]["lifetime"]["cookies"]/(10**12))))-1)/2)
    profiles[profile_id]["current"] = mk_new_current(buildings, upgrades)
    print >>sys.stderr, "handled soft reset; shards=%s" % (profiles[profile_id]["lifetime"]["shards"],)
    




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
    return "%s -- Base DPS = %s\n%s" % (name, fmt(dps), descr)


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
        descr = "Requires %s total donut" % (fmt(cnt))
    else:
        descr = "Requires %s %s" % (fmt(cnt), buildings[building_id]["name"])
    flavor = upgrades[upgrade_id].get("flavor", "...")
    building_id = upgrades[upgrade_id]["target"]
    if upgrades[upgrade_id].get("incr_pct", "") != "":
        if building_id == "click":
            descr2 = "Multiplies DPC by %s." % (upgrades[upgrade_id]["incr_pct"])
        elif building_id == "*":
            descr2 = "Multiplies both DPS and DPC by %s." % (upgrades[upgrade_id]["incr_pct"])
        else:
            descr2 = "Multiplies %s's DPS by %s." % (buildings[building_id]["name"], upgrades[upgrade_id]["incr_pct"])
    if upgrades[upgrade_id].get("incr_base_cps", "") != "":
        if building_id == "click":
            descr2 = "Adds to DPC by %s donuts." % (fmt(upgrades[upgrade_id]["incr_base_cps"]))
        elif building_id == "*":
            descr2 = "Adds to DPS by %s donuts." % (upgrades[upgrade_id]["incr_pct"])
        else:
            descr2 = "Adds %s donuts to %s's base DPS." % (fmt(upgrades[upgrade_id]["incr_base_cps"]), buildings[building_id]["name"])
    
    if cnt > 1:
        descr += "s."
    else:
        descr += "."
    return "%s -- %s donuts -- %s -- %s\n%s" % (name, fmt(upgrades[upgrade_id]["cost"]), descr, descr2,flavor)



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


