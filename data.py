import json
from typing import Optional


def welcome() -> None:
    print(
        "Welcome to a Post-Apocalyptic version of NYJC. After oppenheimer dropped the third bomb, Singapore was devastated. You desperately want your A-level results located in the NYJC Staff Room. You reach NYJC only to realise it has been partially destroyed by the explosions. The main gate is overun with mutant creatures, hence you need to enter through the only available entry, the sheltered court face entry system. You have to navigate a post-apocolyptic NYJC overuned with mutant creatures, collect weapons, pick up key items, and ultimately collect your 'A' level certificate from the final boss. "
    )


def win() -> None:
    print(
        "As you clutched your 'A' level certificate, a rush of emotions sweeps you over. This piece of paper represented more than just your academic achievement; it symbolized your indomitable spirit, adaptability, and the unwavering commitment to your dreams even amidst the harshest of circumstances. Your journey through the post-apocalyptic school was not just a quest for a certificate, but a testament to the power of education and the human spirit. Congratulations player, you have beat the Final Boss and collected your 'A' levels certificate."
    )


def loseboss() -> None:
    print(
        "With a heavy heart, you stand amidst the debris and shadows of the post-apocalyptic school, your quest to retrieve your 'A' level certificate from the clutches of the final boss having ended in defeat. Despite your long and arduous exploration, your efforts were not enough to overcome the challenges that awaited you within these decaying walls. As you gaze around the abandoned school, the weight of disappointment settles upon your shoulders. The corridors that once echoed with the laughter and footsteps of students now reverberate with the emptiness of a world forever changed. The final boss, a formidable adversary, had proven to be an insurmountable obstacle, guarding the precious certificates within the heart of this fallen institution. You lose."
    )


def loseothers() -> None:
    print(
        "Unfortunately, your quest to retrieve your 'A' level certificate has ended and you have died. You recall the trials you faced – the treacherous journey through darkened classrooms, the tense encounters with remnants of security systems, and the labyrinthine corridors that seemed to shift and deceive. Each step you took was a testament to your determination, but alas, the odds were not in your favor this time. With a sigh, you realize that the certificate, a symbol of your achievements and hard work, remains beyond your grasp. You lose."
    )


class Player:

    def __init__(self):
        self.health = 100
        self.ap = 5
        self.weapons = Inventory("weapons")
        self.keyitems = Inventory("keyitems")
        self.healthitems = Inventory("health")

    def update_health(self, value: int) -> None:
        self.health += value

    def get_health(self) -> int:
        return self.health


class Inventory:

    def __init__(self, category: str):
        self.category = category
        self.contents = []

    def add(self, item) -> None:
        if item.name in self.contents:
            return
        else:
            self.contents.append(item)

    def get_inventory(self) -> dict:
        return self.contents


class Item:

    def __init__(self, name, description, category):
        self.name = name
        self.description = description
        self.category = category


class Weapon(Item):

    def __init__(self, name, description, damage, category):
        super().__init__(name, description, category)
        self.ap = damage

    @classmethod
    def from_dict(cls, record: dict) -> "Weapon":
        object = cls(record["name"], record["description"], record["damage"],
                     record["category"])
        return object


class KeyItem(Item):

    def __init__(self, name, description, usage, category):
        super().__init__(name, description, category)
        self.usage = usage

    @classmethod
    def from_dict(cls, record: dict) -> "KeyItem":
        object = cls(record["name"], record["description"], record["usage"],
                     record["category"])
        return object


class HealthItem(Item):

    def __init__(self, name, description, health, category):
        super().__init__(name, description, category)
        self.health = health

    @classmethod
    def from_dict(cls, record: dict) -> "HealthItem":
        object = cls(record["name"], record["description"], record["healing"],
                     record["category"])
        return object


weapons = []
keyitems = []
healthitems = []
allitems = []

with open("items.json", "r") as a:
    items: dict = json.load(a)
    for weapon_data in items["weapons"]:
        weapon = Weapon.from_dict(weapon_data)
        weapons.append(weapon)
        allitems.append(weapon)
    for keyitem_data in items["key_items"]:
        keyitem = KeyItem.from_dict(keyitem_data)
        keyitems.append(keyitem)
        allitems.append(keyitem)
    for healthitem_data in items["health_items"]:
        healthitem = HealthItem.from_dict(healthitem_data)
        healthitems.append(healthitem)
        allitems.append(healthitem)


def get_healthitem(name: str) -> Optional["HealthItem "]:
    for item in healthitems:
        if item.name == name:
            return item
    return None


def get_keyitem(name: str) -> Optional["KeyItem"]:
    for item in keyitems:
        if item.name == name:
            return item
    return None


def get_weapon(name: str) -> Optional["Weapon"]:
    for item in weapons:
        if item.name == name:
            return item
    return None


class Monster:

    def __init__(self, name: str, description: str, health: int, ap: int,
                 items: list[str], slot: int):
        self.name = name
        self.health = health
        self.ap = ap
        self.description = description
        self.items = items
        self.slot = slot

    def update_health(self, value: int) -> None:
        self.health += value

    def get_health(self) -> int:
        return self.health

    @classmethod
    def from_dict(cls, record: dict) -> "Monster":
        assert "items" in record, f"Error: {record['name']} does not have items"
        return cls(record["name"], record["description"], record["health"],
                     record["ap"], record["items"], record["slot"])


monsters = []
with open("creatures.json", "r") as m:
    monsterlist = json.load(m)
    for record in monsterlist:
        monster = Monster.from_dict(record)
        monsters.append(monster)


def get_monster(name: str) -> Optional["Monster"]:
    for monster in monsters:
        if monster.name == name:
            return monster
    return None


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


rooms = []
with open("room.json", "r") as f:
    roomlist = json.load(f)
    for record in roomlist:
        room = Room.from_dict(record)
        rooms.append(room)


def get_room(name: str) -> Optional["Room"]:
    for room in rooms:
        if room.name == name:
            return room
    return None


class Action:

    def __init__(self, name: str):
        self.name = name


EXPLORE = Action("Explore")
GOTO_ROOM = Action("Go To")
USE_ITEM = Action("Use Item")
ATTACK = Action("Attack")


def actionslist() -> list[Action]:
    actionslist = [EXPLORE, GOTO_ROOM, USE_ITEM, ATTACK]
    return actionslist
