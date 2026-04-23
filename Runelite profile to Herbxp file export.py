# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:54:45 2026

@author: Kelsey
"""

import os
import re
import time
import json
import urllib.request
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
RUNELITE_PROFILE = r"C:\Users\XXXXXX\.runelite\profiles2\default-966121055985200.properties"
OUTPUT_DIR = r"C:\Users\XXXXX\Desktop\osrs_output"

ITEMID_JAVA = r"C:\Users\XXXXX\Documents\ItemID.java"
ITEMID_URL = "https://raw.githubusercontent.com/runelite/runelite/master/runelite-api/src/main/java/net/runelite/api/ItemID.java"
ITEMID_REFRESH_DAYS = 7


# -----------------------------
# ITEM NAME LOADING
# -----------------------------
def update_itemid_file():
    needs = True
    if os.path.exists(ITEMID_JAVA):
        age = (time.time() - os.path.getmtime(ITEMID_JAVA)) / 86400
        needs = age >= ITEMID_REFRESH_DAYS

    if needs:
        Path(ITEMID_JAVA).parent.mkdir(parents=True, exist_ok=True)
        try:
            print("Updating ItemID.java...")
            urllib.request.urlretrieve(ITEMID_URL, ITEMID_JAVA)
        except Exception as e:
            print(f"Failed to update ItemID.java: {e}")


def load_item_names():
    update_itemid_file()
    item_map = {}

    with open(ITEMID_JAVA, "r", encoding="utf-8") as f:
        content = f.read()

    matches = re.findall(
        r'public\s+static\s+final\s+int\s+([A-Z0-9_]+)\s*=\s*(\d+);',
        content
    )

    for name, item_id in matches:
        item_map[str(item_id)] = name.replace("_", " ").title()

    return item_map


ITEM_NAMES = load_item_names()


def get_item_name(item_id):
    return ITEM_NAMES.get(str(item_id), f"Item {item_id}")


# -----------------------------
# BANK PARSING
# -----------------------------
def extract_bank_items():

    with open(RUNELITE_PROFILE, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r'bankMemory\.currentList=(.+)', content)

    if not match:
        print("No bankMemory found")
        return []

    raw = match.group(1)

    if "itemData" in raw:
        raw = raw.split("itemData", 1)[1]

    raw = raw.replace('"', '').replace('\\', '')

    numbers = re.findall(r'\d+', raw)

    items = []

    for i in range(0, len(numbers) - 1, 2):
        item_id = int(numbers[i])
        qty = int(numbers[i + 1])

        items.append({
            "item_id": item_id,
            "quantity": qty,
            "item_name": get_item_name(item_id)
        })

    return items


# -----------------------------
# HERBLORE DATASET (CORE)
# -----------------------------
HERBLORE_ACTIONS = [

# -----------------------------
# CLEANING (grimy → clean)
# -----------------------------
{"name":"Clean guam","inputs":{199:1},"outputs":{249:1},"xp":2.5},
{"name":"Clean marrentill","inputs":{201:1},"outputs":{251:1},"xp":3.8},
{"name":"Clean tarromin","inputs":{203:1},"outputs":{253:1},"xp":5},
{"name":"Clean harralander","inputs":{205:1},"outputs":{255:1},"xp":6.3},
{"name":"Clean ranarr","inputs":{207:1},"outputs":{257:1},"xp":7.5},
{"name":"Clean toadflax","inputs":{3049:1},"outputs":{2998:1},"xp":8},
{"name":"Clean irit","inputs":{209:1},"outputs":{259:1},"xp":8.8},
{"name":"Clean avantoe","inputs":{211:1},"outputs":{261:1},"xp":10},
{"name":"Clean kwuarm","inputs":{213:1},"outputs":{263:1},"xp":11.3},
{"name":"Clean snapdragon","inputs":{3051:1},"outputs":{3000:1},"xp":11.8},
{"name":"Clean cadantine","inputs":{215:1},"outputs":{265:1},"xp":12.5},
{"name":"Clean lantadyme","inputs":{2485:1},"outputs":{2481:1},"xp":13.1},
{"name":"Clean dwarf weed","inputs":{217:1},"outputs":{267:1},"xp":13.8},
{"name":"Clean torstol","inputs":{219:1},"outputs":{269:1},"xp":15},

# -----------------------------
# UNFINISHED POTIONS
# -----------------------------
{"name":"Guam potion (unf)","inputs":{249:1,227:1},"outputs":{91:1},"xp":0},
{"name":"Marrentill potion (unf)","inputs":{251:1,227:1},"outputs":{93:1},"xp":0},
{"name":"Tarromin potion (unf)","inputs":{253:1,227:1},"outputs":{95:1},"xp":0},
{"name":"Harralander potion (unf)","inputs":{255:1,227:1},"outputs":{97:1},"xp":0},
{"name":"Ranarr potion (unf)","inputs":{257:1,227:1},"outputs":{99:1},"xp":0},
{"name":"Toadflax potion (unf)","inputs":{2998:1,227:1},"outputs":{3002:1},"xp":0},
{"name":"Irit potion (unf)","inputs":{259:1,227:1},"outputs":{101:1},"xp":0},
{"name":"Avantoe potion (unf)","inputs":{261:1,227:1},"outputs":{103:1},"xp":0},
{"name":"Kwuarm potion (unf)","inputs":{263:1,227:1},"outputs":{105:1},"xp":0},
{"name":"Snapdragon potion (unf)","inputs":{3000:1,227:1},"outputs":{3004:1},"xp":0},
{"name":"Cadantine potion (unf)","inputs":{265:1,227:1},"outputs":{107:1},"xp":0},
{"name":"Lantadyme potion (unf)","inputs":{2481:1,227:1},"outputs":{2483:1},"xp":0},
{"name":"Dwarf weed potion (unf)","inputs":{267:1,227:1},"outputs":{109:1},"xp":0},
{"name":"Torstol potion (unf)","inputs":{269:1,227:1},"outputs":{111:1},"xp":0},

# -----------------------------
# FINISHED POTIONS
# -----------------------------
{"name":"Attack potion","inputs":{91:1,221:1},"xp":25},
{"name":"Anti-poison","inputs":{93:1,235:1},"xp":37.5},
{"name":"Strength potion","inputs":{95:1,225:1},"xp":50},
{"name":"Serum 207","inputs":{97:1,592:1},"xp":50},
{"name":"Restore potion","inputs":{97:1,223:1},"xp":62.5},
{"name":"Energy potion","inputs":{97:1,1975:1},"xp":67.5},
{"name":"Defence potion","inputs":{99:1,239:1},"xp":75},
{"name":"Agility potion","inputs":{3002:1,2152:1},"xp":80},
{"name":"Combat potion","inputs":{97:1,9736:1},"xp":84},
{"name":"Prayer potion","inputs":{99:1,231:1},"xp":87.5},
{"name":"Super attack","inputs":{101:1,221:1},"xp":100},
{"name":"Super anti-poison","inputs":{101:1,235:1},"xp":106.3},
{"name":"Fishing potion","inputs":{101:1,231:1},"xp":112.5},
{"name":"Super energy","inputs":{103:1,2970:1},"xp":117.5},
{"name":"Hunter potion","inputs":{103:1,10111:1},"xp":120},
{"name":"Super strength","inputs":{105:1,225:1},"xp":125},
{"name":"Super restore","inputs":{3004:1,223:1},"xp":142.5},
{"name":"Super defence","inputs":{107:1,239:1},"xp":150},
{"name":"Antidote+","inputs":{2483:1,5937:1},"xp":155},
{"name":"Ranging potion","inputs":{109:1,245:1},"xp":162.5},
{"name":"Magic potion","inputs":{2483:1,3138:1},"xp":172.5},
{"name":"Zamorak brew","inputs":{111:1,247:1},"xp":175},
{"name":"Saradomin brew","inputs":{3004:1,6693:1},"xp":180},
{"name":"Super combat potion","inputs":{2483:1,3000:1},"xp":150},  # simplified (real is composite)
]


# -----------------------------
# OPTIMIZER
# -----------------------------
def optimize_herblore(items):

    bank = {i["item_id"]: i["quantity"] for i in items}
    total_xp = 0
    actions_log = []

    actions = sorted(HERBLORE_ACTIONS, key=lambda x: x["xp"], reverse=True)

    for action in actions:

        while True:

            possible = []

            for item_id, req in action["inputs"].items():
                if bank.get(item_id, 0) < req:
                    possible = [0]
                    break
                possible.append(bank[item_id] // req)

            craftable = min(possible) if possible else 0

            if craftable <= 0:
                break

            # consume inputs
            for item_id, req in action["inputs"].items():
                bank[item_id] -= req

            # add outputs if exist
            if "outputs" in action:
                for out_id, qty in action["outputs"].items():
                    bank[out_id] = bank.get(out_id, 0) + qty

            total_xp += action["xp"]
            actions_log.append(action["name"])

    return total_xp, actions_log, bank


def write_outputs(items, xp, actions, remaining):

    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # BANK FILES
    # -----------------------------
    with open(out_dir / "bank_items.txt", "w", encoding="utf-8") as f:
        for i in items:
            f.write(f"{i['item_id']},{i['quantity']},{i['item_name']}\n")

    with open(out_dir / "bank_items.json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=4)

    # -----------------------------
    # HERBLORE JSON
    # -----------------------------
    result = {
        "total_xp": xp,
        "actions_count": len(actions),
        "remaining_bank": remaining
    }

    with open(out_dir / "herblore_optimization.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    # -----------------------------
    # ACTION SUMMARY
    # -----------------------------
    action_xp_map = {a["name"]: a["xp"] for a in HERBLORE_ACTIONS}

    action_summary = {}

    for action in actions:
        if action not in action_summary:
            action_summary[action] = {
                "count": 0,
                "xp_each": action_xp_map.get(action, 0)
            }
        action_summary[action]["count"] += 1

    # Calculate total XP per action
    for name in action_summary:
        data = action_summary[name]
        data["total_xp"] = data["count"] * data["xp_each"]

    # Sort by total XP descending (better insight)
    sorted_actions = sorted(
        action_summary.items(),
        key=lambda x: x[1]["total_xp"],
        reverse=True
    )

    # -----------------------------
    # FINAL PRODUCTS
    # -----------------------------
    final_products = {}

    # Actions WITHOUT outputs = final products
    final_action_names = {
        a["name"] for a in HERBLORE_ACTIONS if "outputs" not in a
    }

    for action in actions:
        if action in final_action_names:
            final_products[action] = final_products.get(action, 0) + 1

    # -----------------------------
    # TXT OUTPUT
    # -----------------------------
    txt_path = out_dir / "herblore_optimization.txt"

    with open(txt_path, "w", encoding="utf-8") as f:

        f.write("=== HERBLORE OPTIMIZATION ===\n\n")

        f.write(f"Total XP: {xp}\n")
        f.write(f"Total Actions Performed: {len(actions)}\n")
        f.write(f"Unique Actions: {len(action_summary)}\n\n")

        # -----------------------------
        # ACTION BREAKDOWN
        # -----------------------------
        f.write("=== ACTION BREAKDOWN (Sorted by XP) ===\n")

        for name, data in sorted_actions:
            f.write(
                f"{name}: {data['count']} "
                f"({data['xp_each']} xp each → {data['total_xp']} xp)\n"
            )

        # -----------------------------
        # FINAL PRODUCTS
        # -----------------------------
        f.write("\n=== FINAL PRODUCTS ===\n")

        for name, count in sorted(
            final_products.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            f.write(f"{name}: {count}\n")

        # -----------------------------
        # REMAINING MATERIALS
        # -----------------------------
        f.write("\n=== REMAINING MATERIALS ===\n")

        for item_id, qty in remaining.items():
            if qty <= 0:
                continue
            f.write(f"{item_id},{qty},{get_item_name(item_id)}\n")

    print(f"\nTotal Herblore XP: {xp}")
    print(f"Output directory: {out_dir}")


# -----------------------------
# MAIN
# -----------------------------
def main():
    items = extract_bank_items()
    if not items:
        return

    xp, actions, remaining = optimize_herblore(items)
    write_outputs(items, xp, actions, remaining)


if __name__ == "__main__":
    main()