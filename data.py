import json
import random
from typing import Optional


class Player:

    def __init__(self):
        self.health = 100
        self.ap = 5
        self.weapons = Inventory("weapons")
        self.keyitems = Inventory("keyitems")
        self.healthitems = Inventory("health")

    def is_dead(self) -> bool:
        return self.health <= 0

    def status(self) -> str:
        return f"HEALTH: {self.get_health()}"

    def update_health(self, value: int) -> None:
        self.health += value

    def get_health(self) -> int:
        return self.health


class Inventory:

    def __init__(self, category: str):
        self.category = category
        self._contents = []

    def add(self, item) -> None:
        if item.name in self.contents():
            return
        else:
            self._contents.append(item)

    def contents(self) -> list[str]:
        return [item.name for item in self._contents]

    def count(self) -> int:
        return len(self._contents)

    def get(self, name: str):
        for item in self._contents:
            if item.name == name:
                return name

    def is_empty(self) -> bool:
        return self.count() == 0

    def remove(self, name: str) -> bool:
        """Remove item with the given name.
        Return True if successfully removed, otherwise False
        """
        if name not in self.contents():
            return False
        index = self.contents().index(name)
        del self._contents[index]
        return True


class Item:

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Weapon(Item):

    def __init__(self, name, description, damage):
        super().__init__(name, description)
        self.ap = damage

    def status(self) -> str:
        result = ("-" * 5) + self.name + "'s Status" + ("-" * 5)
        result += "\n"
        result += f"DESCRIPTION: {self.description}"
        result += "\n"
        result += "ATTACK BUFF: +{self.ap}"
        return result

    @classmethod
    def from_dict(cls, record: dict) -> "Weapon":
        object = cls(record["name"], record["description"], record["damage"])
        return object


class KeyItem(Item):

    def __init__(self, name, description, usage):
        super().__init__(name, description)
        self.usage = usage

    def status(self) -> str:
        result = ("-" * 5) + self.name + "'s Status" + ("-" * 5)
        result += "\n"
        result += f"DESCRIPTION: {self.description}"
        result += "\n"
        result += f"USAGE:{self.usage}"
        return result

    @classmethod
    def from_dict(cls, record: dict) -> "KeyItem":
        object = cls(record["name"], record["description"], record["usage"])
        return object


class HealthItem(Item):

    def __init__(self, name, description, health):
        super().__init__(name, description)
        self.health = health

    def status(self) -> str:
        result = ("-" * 5) + self.name + "'s Status" + ("-" * 5)
        result += "\n"
        result += f"DESCRIPTION: {self.description}"
        result += "\n"
        result += f"HEALTH:{self.health}"
        return result
    
    @classmethod
    def from_dict(cls, record: dict) -> "HealthItem":
        object = cls(record["name"], record["description"], record["healing"])
        return object


class Monster:

    def __init__(self, name: str, description: str, health: int, ap: int,
                 items: list[str], slot: int):
        self.name = name
        self.health = health
        self.ap = ap
        self.description = description
        self.items = items
        self.slot = slot

    def is_dead(self) -> bool:
        return self.health <= 0

    def status(self) -> str:
        result = f"You found the {self.name}!"
        result += "\n"
        result += f"DESCRIPTION: {self.description}"
        return result

    def update_health(self, value: int) -> None:
        self.health += value

    def get_health(self) -> int:
        return self.health

    @classmethod
    def from_dict(cls, record: dict) -> "Monster":
        assert "items" in record, f"Error: {record['name']} does not have items"
        return cls(record["name"], record["description"], record["health"],
                     record["ap"], record["items"], record["slot"])


class Room:

    def __init__(self,
                 name: str,
                 descriptions: list[str],
                 monster: str,
                 max_visits: int,
                 visit_count: int = 0):
        self.name = name
        self.descriptions = descriptions
        self.monster = monster
        self.max_visits = max_visits
        self.visit_count = visit_count

    def description(self) -> str:
        if self.is_fully_visited():
            return "There is nothing left to explore."
        return self.descriptions[self.visit_count]

    def status(self) -> str:
        result = "-----EXPLORED RESULTS-----"
        result += "\n"
        result += self.description()
        return result

    def visit(self):
        self.visit_count += 1

    def is_fully_visited(self) -> bool:
        return self.visit_count < self.max_visits

    def add_item(self) -> None:
        print("Sorry you can't do that")

    def remove_item(self, name: str) -> None:
        pass

    @classmethod
    def from_dict(cls, record: dict) -> "Room":
        max_visits = len(record["descriptions"])

        object = cls(record["name"],
                     record["descriptions"],
                     record.get("monster", None),
                     max_visits)
        return object


weapons = {}
keyitems = {}
healthitems = {}
monsters = {}
rooms = {}

with open("items.json", "r") as a:
    items: dict = json.load(a)
for weapon_data in items["weapons"]:
    weapon = Weapon.from_dict(weapon_data)
    weapons[weapon.name] = weapon
for keyitem_data in items["key_items"]:
    keyitem = KeyItem.from_dict(keyitem_data)
    keyitems[keyitem.name] = keyitem
for healthitem_data in items["health_items"]:
    healthitem = HealthItem.from_dict(healthitem_data)
    healthitems[healthitem.name] = healthitem

with open("creatures.json", "r") as m:
    monsterlist = json.load(m)
for record in monsterlist:
    monster = Monster.from_dict(record)
    monsters[monster.name] = monster

with open("room.json", "r") as f:
    roomlist = json.load(f)
for record in roomlist:
    room = Room.from_dict(record)
    rooms[room.name] = room

def get_healthitem(name: str) -> Optional["HealthItem"]:
    return healthitems.get(name, None)

def get_random_healthitem() -> "HealthItem":
    return random.choice(healthitems.values())

def get_keyitem(name: str) -> Optional["KeyItem"]:
    return keyitems.get(name, None)

def get_weapon(name: str) -> Optional["Weapon"]:
    return weapons.get(name, None)

def get_item(name: str) -> Optional["Item"]:
    """Search for a health item, key item, or weapon"""
    item = get_healthitem(name)
    if item:
        return item
    item = get_keyitem(name)
    if item:
        return item
    item = get_weapon(name)
    if item:
        return item
    return None        

def get_monster(name: str) -> Optional["Monster"]:
    return monsters.get(name, None)

def get_room(name: str) -> Optional["Room"]:
    return rooms.get(name, None)

def room_names() -> list[str]:
    return list(rooms.keys())


EXPLORE = "Explore"
GOTO_ROOM = "Go To"
USE_ITEM = "Use Item"
ATTACK = "Attack"

_actions = [EXPLORE, GOTO_ROOM, USE_ITEM, ATTACK]

def get_actions() -> list[str]:
    return _actions.copy()
