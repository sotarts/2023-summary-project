#Test move room works
#Test attack monster works (game ends when you die)
#Test monster drop works

import random

import action
import data
import text


# Prompt helpers
def prompt_valid_choice(options: list[str], question: str, show=True) -> str:
    """Takes in a list of strs and a question, returns the chosen object"""
    if show:
        for i, option in enumerate(options, start=1):
            print(f"{i}: {option}")

    userinput = None
    while not userinput:
        userinput = input(f"{question} (SELECT A NUMBER): ").strip()
        if userinput in options:
            break
        else:
            userinput = None
            print(text.input_invalid)
            print()
    print("")
    return userinput


# Combat helpers

def generate_numbers(last: int) -> list[int]:
    """Return a list of numbers from 1 to last"""
    assert last > 0
    return list(range(1, last))

def dice_roll(sides: int, chance: int) -> bool:
    """Simulate a dice roll for success.

    Arguments
    ---------
    sides: int
      number of sides the dice has.

    chance: int
      number of sides that yield success

    Return
    ------
    True if successful, False otherwise
    """
    assert sides > 1
    assert chance <= sides
    return 1 <= random.randint(1, sides) <= chance

def dice_check(sides: int, target: int) -> bool:
    """Simulate a dice roll for a target value.

    Arguments
    ---------
    sides: int
      number of sides the dice has.

    target: int
      number to aim for

    Return
    ------
    True if dice roll matches target, False otherwise
    """
    return random.randint(1, sides) == target


START_ROOM = "Overgrown Sheltered Courts"
START_WEAPON = "Basketball Shoe"
BOSS_ROOM = "Abandoned Staff Room"
BOSS_KEY = "Cat"
BOSS_NAME = "Final Boss"
GATE_ROOM = "Forgotten Library"
GATE_KEY = "Old Staff Key Card"


class Game:
    """Encapsulates the main game"""

    def __init__(self) -> None:
        self.player = data.Player(health=100, ap=5)
        self.current_room = data.get_room(START_ROOM)
        assert self.current_room is not None, "Start room could not be found"

        # Add first weapon; fists into the weapons inventory
        self.player.weapons.add(data.get_weapon(START_WEAPON))

    def end_game(self) -> None:
        if self.player.is_dead():
            if self.current_room == data.get_room(BOSS_ROOM):
                print(text.loseboss())
            else:
                print(text.loseothers())
        else:
            boss = data.get_monster(BOSS_NAME)
            if boss.is_dead():
                print(text.win())

    def gameover(self) -> bool:
        """Check if game is over, if the player win, win method is called, while if player lose, losing method is called BOTH is asked to restart"""
        if self.player.is_dead():
            return True
        boss = data.get_monster(BOSS_NAME)
        if boss.is_dead():
            return True
        return False

    def prompt_room(self) -> str:
        """Prompts player to pick a room to visit.
        Return player's choice.
        """
        room_names = data.room_names()
        room_names.remove(BOSS_ROOM)
        room_name = prompt_valid_choice(room_names, text.prompt_room)
        return room_name

    def goto_room(self, room_name: str) -> None:
        """Update player's location to given room."""
        self.current_room = data.get_room(room_name)

    def attack(self) -> None:
        """WHOLE ATTACKING SEQUENCE, attacks monster in current room. """
        #---ATTACK LOOP---
        monster = data.get_monster(self.current_room.monster)
        while monster and not self.player.is_dead():
            self.show_layout(monster.slot)
            dodge_slot = prompt_valid_choice(
                generate_numbers(2),
                text.prompt_dodge,
                False
            )
            attack_slots = generate_numbers(monster.slot + 1)

            attack_slot = prompt_valid_choice(
                attack_slots, text.prompt_square,
                False)
            choice = prompt_valid_choice(self.player.weapons.contents(),
                                 text.prompt_weapon)
            chosen_weapon = self.player.weapons.get(choice)

            print(text.header("BATTLE RESULT", width=23))
            if dice_check(sides=monster.slot, target=attack_slot):
                dmg = self.player.ap * chosen_weapon.ap
                monster.take_damage(dmg)
                print(text.attack_success(dmg))
            else:
                print(text.attack_fail)

            if not monster.is_dead():
                if dice_check(sides=4, target=dodge):
                    self.player.take_damage(monster.ap)
                    print(text.dodge_fail(monster.ap))
                else:
                    print(text.dodge_success)
                    print()
            else:
                print(text.monster_killed)
                print()
                print(text.header("SPOILS", width=16))
                self.pickup_loot(monster)
                monster = None

    def prompt_item(self) -> str | None:
        """Prompt player to choose an item to use.
        Return item name.
        """
        item_type = prompt_valid_choice(["Health Items", "Key Items"],
                                text.prompt_use_type)
        if item_type == "Health Items":
            if self.player.healthitems.is_empty():
                print(text.items_empty("health items"))
                return None
            choice = prompt_valid_choice(self.player.healthitems.contents(),
                                 text.prompt_use_item)
            return choice

        elif item_type == "Key Items":
            if self.player.keyitems.is_empty():
                print(text.items_empty("key items"))
                return None
            choice = prompt_valid_choice(self.player.keyitems.contents(),
                                 text.prompt_use_item)
            return choice
        raise ValueError(f"Error: invalid choice {item_type}")

    def use_item(self, item_name: str) -> None:
        """Use the given item"""
        if item_name in self.player.healthitems.contents():
            self.use_healthitem(item_name)
        elif item_name in self.player.keyitems.contents():
            self.use_keyitem(item_name)
        raise ValueError(f"{item_name}: Not a valid item in player's inventory")

    def use_healthitem(self, item_name: str) -> None:
        """Updates the player health using the chosen item"""
         item = self.player.healthitems.get(item_name)
        self.player.healthitems.remove(item.name)
        self.player.heal(item.health)
        print(text.use_item(item.name, f"healed {item.health} HP"))

    def use_keyitem(self, item_name: str) -> None:
        """Takes in the keyitem chosen and use it if possible"""
        item = self.player.keyitems.get(item_name)
        if item.name == GATE_KEY:
            if self.current_room == data.get_room(GATE_ROOM):
                self.goto_room(BOSS_ROOM)
                print(text.use_boss_key)
            else:
                print(text.use_wrong_key)

        if item.name == BOSS_KEY:
            if self.current_room == data.get_room(BOSS_ROOM):
                print(text.boss_encounter)
                boss = data.get_monster(BOSS_NAME)
                print(boss.status())
                self.attack()
            else:
                print(text.no_boss_encounter)

    def pickup_loot(self, monster: data.Monster) -> None:
        """Check if monster have loot and add it to the respective inventories"""
        if not monster.items:
            return
        for item_name in monster.items:
            item = data.get_item(item_name)
            if item:
                self.player.take(item)
            else:
                print(text.item_error(item_name))
                continue
            print(text.take_item(item.name))
            print(item.status())

    def show_layout(self, slot: int) -> None:
        """Prints the attacking layout"""
        monster = data.get_monster(self.current_room.monster)
        divider = " |"
        spacer = ((slot * 2 + 1 - 7) // 2) * " "
        print()
        print(text.header("ATTACKING", width=29))
        print(f"{monster.name} HP: {monster.health}")
        print("\t\t" + "_" * (slot * 2 + 1))
        print(f"\t\t|{divider * slot}")
        print("\t\t" + " " + " ".join([str(i) for i in range(1, slot + 1)]))
        print("\n" * 2)
        print("\t\t" + spacer + ("_" * (5)))
        print("\t\t" + spacer + f"|{divider * 2}")
        print("\t\t" + spacer + " " + " ".join([str(i) for i in range(1, 3)]))
        print(f"Your HP: {self.player.health}")
        print("-" * 30 + "\n")

    def get_possible_actions(self) -> list[str]:
        """Returns a list of possible actions"""
        if self.current_room == data.get_room(BOSS_ROOM):
            return [action.EXPLORE, action.GOTO_ROOM, action.USE_ITEM]
        if not self.current_room.is_fully_visited():
            return [action.EXPLORE, action.GOTO_ROOM, action.USE_ITEM]
        monster = data.get_monster(self.current_room.monster)
        if monster and not monster.is_dead():
            print(monster.status())
            return [action.ATTACK, action.USE_ITEM]
        return [action.EXPLORE, action.GOTO_ROOM, action.USE_ITEM]

    def get_randomised_loot(self) -> Optional[data.Item]:
        """Determines the chance of returning a random health item"""
        found_item = None
        if self.current_room.visit_count <= 2:
            if dice_roll(sides=10, chance=1):
                found_item = data.get_random_healthitem()

        elif self.current_room.visit_count <= 4:
            if dice_roll(sides=4, chance=1:
                found_item = data.get_random_healthitem()

        else:
            if dice_roll(sides=4, chance=1:
                found_item = data.get_random_healthitem()
        if found_item:
            print(text.found_item(found_item.name)
        return found_item

    def execute_action(self, action: str) -> None:
        """Execute chosen action"""
        if action == action.EXPLORE:
            #Prints description of explore, randomise loot, and increments ec
            print(self.current_room.status())
            loot = self.get_randomised_loot()
            if loot:
                print(loot.status())
                self.player.healthitems.add(loot)
            self.current_room.visit()

        elif action == action.GOTO_ROOM:
            #change room and print room status
            room_name = self.prompt_room()
            self.goto_room(room_name)
            print(self.current_room.status())
            self.current_room.visit()

        elif action == action.USE_ITEM:
            choice = self.prompt_item()
            if choice:
                self.use_item(choice)

        elif action == action.ATTACK:
            self.attack()

    def run(self) -> None:
        """Run the game loop"""
        #-----game loop--------
        #welcome message
        text.welcome()
        while not self.gameover():
            #Display action
            print(text.divider(width=60))
            print(self.player.status())
            print(f"CURRENT ROOM: {self.current_room.name}")
            #Get possible actions
            possible_actions = self.get_possible_actions()
            #Get chosen action
            action = prompt_valid_choice(possible_actions, text.prompt_action)
            #Execute action
            self.execute_action(action)
        # End the game
        self.end_game()
