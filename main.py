# main.py
import random
from hero import Hero
from monster import Monster
import functions
import os
import platform

print(f"Operating System: {os.name}")
print(f"Python Version: {platform.python_version()}")

small_dice_options = list(range(1, 7))
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]
loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves"]
belt = []
monster_powers = {"Fire Magic": 2, "Freeze Time": 4, "Super Hearing": 6}

last_game_result, monsters_killed_line = functions.load_game()
if monsters_killed_line:
    try:
        monsters_killed = int(monsters_killed_line.split(": ")[1])
        print(f"Total monsters killed: {monsters_killed}")
    except:
        print("Error loading monster kills.")
else:
    print("No monster kill data found.")

hero = Hero()
monster = Monster()
num_stars = 0

input_invalid = True
i = 0
while input_invalid and i < 5:
    print("    ------------------------------------------------------------------")
    print("    |", end="    ")
    combat_strength = input("Enter your combat Strength (1-6): ").strip()
    print("    |", end="    ")
    m_combat_strength = input("Enter the monster's combat Strength (1-6): ").strip()
    if (not combat_strength.isdigit()) or (not m_combat_strength.isdigit()):
        print("    |    One or more invalid inputs. Player needs to enter integer numbers for Combat Strength    |")
        i += 1
        continue
    combat_strength = int(combat_strength)
    m_combat_strength = int(m_combat_strength)
    if combat_strength not in range(1, 7) or m_combat_strength not in range(1, 7):
        print("    |    Enter a valid integer between 1 and 6 only")
        i += 1
        continue
    input_invalid = False

input("Rolling the dice for your weapon... (Press enter)")
weapon_roll = random.choice(small_dice_options)
combat_strength = min(6, (int(combat_strength) + weapon_roll))
print("    |    The hero\'s weapon is " + str(weapons[weapon_roll - 1]))

hero.combat_strength, monster.combat_strength = functions.adjust_combat_strength(hero.combat_strength, monster.combat_strength)
print(f"Hero health points: {hero.health_points}")
print(f"Monster health points: {monster.health_points}")

for _ in range(2):
    input("Roll for loot (Press enter)")
    loot_options, belt = functions.collect_loot(loot_options, belt)
belt.sort()
print("Your belt contains:", belt)

belt, hero.health_points = functions.use_loot(belt, hero.health_points)

input("Roll for Monster's Magic Power (Press enter)")
power_roll = random.choice(list(monster_powers.keys()))
monster.combat_strength = min(6, monster.combat_strength + monster_powers[power_roll])
print(f"Monster's combat strength is now {monster.combat_strength} using {power_roll}")

print("    ------------------------------------------------------------------")
print("Exploring the area...")
events = ["artifact", "npc", "bandits"]
eligible_events = [event for event in events if (event == "artifact" or (event == "npc" and hero.health_points < 50) or (event == "bandits" and hero.combat_strength > 70))]
random_event = random.choice(eligible_events)

if random_event == "artifact":
    print("    |    You found a Strange Artifact!")
    artifact_effect = random.choice(["strength_up", "health_down", "health_up", "strength_down"])
    if artifact_effect == "strength_up":
        hero.combat_strength += 3
        print("    |    The artifact increased your combat strength!")
    elif artifact_effect == "health_down":
        hero.health_points = max(0, hero.health_points - 10)
        print("    |    The artifact drained your health!")
    elif artifact_effect == "health_up":
        hero.health_points = min(100, hero.health_points + 15)
        print("    |    The artifact healed you!")
    elif artifact_effect == "strength_down":
        hero.combat_strength = max(1, hero.combat_strength - 2)
        print("    |    The artifact weakened you!")
elif random_event == "npc":
    print("    |    You encountered a friendly NPC.")
    if hero.health_points < 50:
        hero.health_points = min(100, hero.health_points + 20)
        print(f"    |    The NPC healed you. Your health is now {hero.health_points}.")
    else:
        hero.combat_strength += 5
        print(f"    |    The NPC granted you power. Your combat strength is now {hero.combat_strength}.")
elif random_event == "bandits":
    print("    |    You encountered bandits!")
    if hero.combat_strength > monster.health_points:
        print("    |    You defeated the bandits and claimed their loot.")
        loot_options, belt = functions.collect_loot(loot_options, belt)
    else:
        print("    |    The bandits defeated you. You lost all your possessions.")
        belt.clear()
        monster.combat_strength += 2

print("    ------------------------------------------------------------------")
print("You meet the monster. FIGHT!! FIGHT !!")
while monster.health_points > 0 and hero.health_points > 0:
    input("Roll to see who strikes first (Press Enter)")
    attack_roll = random.choice(small_dice_options)
    match attack_roll % 2:
        case 0:
            input("The Monster strikes (Press enter)")
            hero.health_points = functions.monster_attacks(monster.combat_strength, hero.health_points)
        case _:
            input("You strike (Press enter)")
            monster.health_points = functions.hero_attacks(hero.combat_strength, monster.health_points)

winner = "Hero" if monster.health_points <= 0 else "Monster"
def get_hero_name():
    for _ in range(5):
        hero_name = input("Enter your Hero's name (in two words): ").strip()
        name_p = hero_name.split()
        if len(name_p) == 2 and all(part.isalpha() for part in name_p):
            s_name = name_p[0][:2] + name_p[1][0]
            print(f"I'm going to call you {s_name} for short.")
            return s_name
        else:
            print("Invalid name. Please enter two words (letters only).")
    return "Hero"

short_name = get_hero_name()
functions.save_game(winner, hero_name=short_name, num_stars=3 if winner == "Hero" else 1)