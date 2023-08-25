import json

def welcome() -> None:
    print( "Welcome to a Post-Apocalyptic version of NYJC. After oppenheimer dropped the third bomb, Singapore was devastated. You desperately want your A-level results located in the NYJC Staff Room. You reach NYJC only to realise it has been partially destroyed by the explosions. The main gate is overun with mutant creatures, hence you need to enter through the only available entry, the sheltered court face entry system. You have to navigate a post-apocolyptic NYJC overuned with mutant creatures, collect weapons, pick up key items, and ultimately collect your 'A' level certificate from the final boss. ")

def win()->None:
    pass

def lose()-> None:
    pass
    
class Player:
    def __init__(self):
        self.health = 100
        self.ap = 5
        self.weapons = Inventory("weapons")
        self.keyitems = Inventory("keyitems")
        self.healthitems = Inventory("health")
        
    def update_health(self, value: int)-> None:
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
    def from_dict(cls, record: dict) -> "Room":
        object = cls(record["name"], record["description"], record["damage"], record["category"])
        return object

class KeyItem(Item):
    def __init__(self, name, description, usage, category):
        super().__init__(name, description, category)
        self.usage = usage

    @classmethod
    def from_dict(cls, record: dict) -> "Room":
        object = cls(record["name"], record["description"], record["usage"], record["category"])
        return object

class HealthItem(Item):
    def __init__(self, name, description, health, category):
        super().__init__(name, description, category)
        self.health = health

    @classmethod
    def from_dict(cls, record: dict) -> "Room":
        object = cls(record["name"], record["description"], record["healing"], record["category"])
        return object

weapons= []
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
        
def get_healthitem(name: str) -> "Room":
    for item in healthitems:
        if item.name == name:
            return item
            
def get_keyitem(name: str) -> "Room":
    for item in keyitems:
        if item.name == name:
            return item

def get_weapon(name: str) -> "Room":
    for item in weapons:
        if item.name == name:
            return item
            
class Monster:
    def __init__(self, name: str, description: str, health: int, ap: int, item: "Item", slot: int):
        self.name = name
        self.health = health
        self.ap = ap
        self.description = description
        self.item = item
        self.slot = slot

    def update_health(self, value: int)-> None:
        self.health += value

    def get_health(self)-> int:
        return self.health

        
    @classmethod
    def from_dict(cls, record: dict) -> "Room":
        if "item" in record:
            items = []
            for item in record["item"]:
                for value in allitems:
                    if value.name == item:
                        items.append(value)
        else:
            items = False
        object = cls(record["name"], record["description"], record["health"], record["ap"], items, record["slot"])
        return object

            
monsters = []
with open("creatures.json", "r") as m:
    monsterlist = json.load(m)
    for record in monsterlist:
        monster = Monster.from_dict(record)
        monsters.append(monster)

def get_monster(name: str) -> "Room":
    for monster in monsters:
        if monster.name == name:
            return monster


class Room:
    def __init__(self, name: str, description: list, monster: object, max_explored: int, explored_counter=0):
        self.name = name
        self.description = description
        self.explored_counter = explored_counter
        self.monster = monster
        self.max_explored = max_explored
        
    def get_ec(self):
        return self.explored_counter

    def increment_ec(self):
        self.explored_counter += 1

    def add_item(self) -> None:
        print("Sorry you can't do that")
    
    def remove_item(self, name: str) -> None:
        pass

    def get_monster(self) -> "Monster":
        return self.monster
        
    def monster_isdead(self) -> None:
        self.monster = False


    @classmethod
    def from_dict(cls, record: dict) -> "Room":
        name = record["name"]
        description = []
        description1 = record["description"]
        description.append(description1)
        description2 = record["description2"]
        description.append(description2)
        description3 = record["description3"]
        description.append(description3)
        if "description4" in record:
            description4 = record["description4"]
            description.append(description4)
        if "description5" in record:
            description5 = record["description5"]
            description.append(description5)
        if "description6" in record:
            description6 = record["description6"]
            description.append(description6)
        if "description7" in record:
            description7 = record["description7"]
            description.append(description7)
        max_explored = record["max_explored"]
        if "monster" in record:
            monster = get_monster(record["monster"])
        else:
            monster = False
            
        object = cls(name, description, monster, max_explored)
        return object
        
        
rooms = []
with open("room.json", "r") as f:
    roomlist = json.load(f)
    for record in roomlist:
        room = Room.from_dict(record)
        rooms.append(room)

def get_room(name: str) -> Room:
    for room in rooms:
        if room.name == name:
            return room

            

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
    
