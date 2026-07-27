#!/usr/bin/env pyhton3
def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(
            artifacts,
            key=lambda artificat: artificat["power"],
            reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: "* " + spell + " *", spells))


def mage_stats(mages: list[dict]) -> dict:
    max_power = max(mages, key=lambda mage: mage["power"])
    min_power = min(mages, key=lambda mage: mage["power"])
    avg_power = round(sum(
        map(lambda mage: mage["power"], mages)) / len(mages), 2)
    return {
        "max_power": max_power["power"],
        "min_power": min_power["power"],
        "avg_power": avg_power
        }


if __name__ == "__main__":
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "Orb"},
        {"name": "Fire Staff", "power": 92, "type": "Staff"},
        {"name": "Ice Wand", "power": 70, "type": "Wand"}
    ]
    mages = [
        {"name": "Gandalf", "power": 90, "element": "Fire"},
        {"name": "Merlin", "power": 60, "element": "Ice"},
        {"name": "Sage", "power": 80, "element": "Earth"}
    ]
    spells = ["fireball", "heal", "shield"]
    print("Testing artifact sorter...")
    artifacts = artifact_sorter(artifacts)
    print(
            f"{artifacts[0]["name"]} ({artifacts[0]["power"]})"
            f" comes before"
            f" {artifacts[1]["name"]} ({artifacts[1]["power"]})")
    print()
    print("Testing power filter...")
    print(" before:")
    print(mages)
    print(" after:")
    print(power_filter(mages, 80))
    print()
    print("Testing spell transformer...")
    spells = spell_transformer(spells)
    for spell in spells:
        print(spell, end=" ")
    print()
    print("Testing mage stats...")
    print(" the mages:")
    print(mages)
    print(mage_stats(mages))
