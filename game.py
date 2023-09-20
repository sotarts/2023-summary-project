#Test move room works
#Test attack monster works (game ends when you die)
#Test monster drop works

import data
import random

class Game:
    """Encapsulates the main game"""
    def __init__(self) -> None:
        self.player = data.Player()
        self.gameover = False
        self.current_room = data.get_room("Overgrown Sheltered Courts")
        assert self.current_room is not None, "Start room could not be found"

        # Add first weapon; fists into the weapons inventory
        self.player.weapons.add(data.get_weapon("Basketball Shoe"))

    def display_status(self, obj: object) -> None:
        """Takes in any object and print the relevant info based on what type the object is."""
        if not obj:
            return
        print(obj.status())
        if isinstance(obj, data.Player):
            print(f"CURRENT ROOM: {self.current_room.name}")

    def check_gameover(self) -> None:
        """Check if game is over, if the player win, win method is called, while if player lose, losing method is called BOTH is asked to restart"""
        if self.player.is_dead():
            if self.current_room == data.get_room("Abandoned Staff Room"):
                data.loseboss()
            else:
                data.loseothers()
            self.gameover = True

        elif data.get_monster("Final Boss").get_health() <= 0:
            data.win()
            self.gameover = True
        else:
            pass
                   
    def prompt(self, data:list[object], question:str, isObjList=True, show=True) -> object:
        """Takes in a list of object and a question, returns the chosen object"""
        if show:
            if isObjList:
                for i in range(len(data)):
                    print(f"{i+1}: {data[i].name}")
            else:
                for i in range(len(data)):
                    print(f"{i+1}: {data[i]}")
    
        userinput = None
        while not userinput:
            userinput = input(f"{question} (SELECT A NUMBER): ")
            if userinput.isdecimal() and int(userinput) < len(data) + 1 and int(userinput) != 0:
                print("")
                return data[int(userinput)-1]
                break
            else:
                userinput = None
                print("That is not a valid input. Please enter again\n")
                
    def move_to_room(self) -> None:
        """Prompts room and update current room based on input of the player"""
        room_data = data.rooms.copy()
        room_data.remove(data.get_room("Abandoned Staff Room"))
        room = self.prompt(room_data, "WHICH ROOM DO YOU WANT TO GO TO?")
        self.current_room = room
  
    def attack(self) -> None:
        """WHOLE ATTACKING SEQUENCE, attacks monster in current room. """
        #---ATTACK LOOP---
        monster = data.get_monster(self.current_room.monster)
        while monster and not self.player.is_dead():
            self.show_layout(monster.slot)
            dodge_slot = self.prompt([1, 2], "You have a chance to dodge, which slot will you like to dodge to?", False, False)
            slot_list = []
            for i in range(1, monster.slot + 1):
                slot_list.append(i)

            attack_slot = self.prompt(slot_list,"Choose which square you would like to attack.", False, False)
            chosen_weapon = self.prompt(self.player.weapons.get_inventory(), "Which weapon do you want to use?")

            print("-----BATTLE RESULT-----")
            if attack_slot == random.randint(1, monster.slot): #change b to max slot of monster
                monster.update_health(self.player.ap * chosen_weapon.ap *-1)
                print(f"You guessed correctly and dealt {self.player.ap * chosen_weapon.ap} damage!")
            else:
                print("Oops, your attack missed the monster..")
                
            if monster.get_health() > 0:
                if random.randint(1,4) == dodge_slot:
                    self.player.update_health(monster.ap * -1)
                    print(f"Uh oh, you ran into the monster's attack path, you lost {monster.ap} HP..")
                else:
                    print("You managed to dodge the monsters attack successfully!\n")
            else:
                print("You have killed the monster!!!\n")
                print("-----SPOILS-----")
                self.pickup_loot(monster)
                monster = None
                
    def use_item(self) -> None:
        item_type = self.prompt(["Health Items", "Key Items"], "WHICH TYPE OF OBJECT DO YOU WANT TO USE?", False)
        if item_type == "Health Items":                 
            if len(self.player.healthitems.get_inventory()) == 0:
                print("You do not have any health items")
                return
            self.use_healthitem(self.prompt(self.player.healthitems.get_inventory(), "WHICH OBJECT DO YOU WANT TO USE?"))
            
        elif item_type == "Key Items":
            if len(self.player.keyitems.get_inventory()) == 0:
                print("You do not have any Key items")
                return
            self.use_keyitem(self.prompt(self.player.keyitems.get_inventory(),"WHICH OBJECT DO YOU WANT TO USE?"))

    def use_healthitem(self, healthitem: object)-> None:
        """Updates the player health using the chosen item"""
        self.player.healthitems.get_inventory().remove(healthitem)
        self.player.update_health(healthitem.health)
        print(f"You used up 1 {healthitem.name} and healed {healthitem.health} HP!")

    def use_keyitem(self, keyitem:object) -> None:
        """Takes in the keyitem chosen and use it if possible"""
        if keyitem.name == "Old Staff Key Card":
            if self.current_room == data.get_room("Forgotten Library"):
                self.current_room = data.get_room("Abandoned Staff Room")
                print("You have accessed the staff room... the Final Boss might be lurking nearby....")
            else:
                print("There is no use for this item in this room. Perhaps you should go to a different room.....")

        if keyitem.name == "Cat":
            if self.current_room == data.get_room("Abandoned Staff Room"):
                print("You summoned the Final Boss.....")
                self.display_status(data.get_monster("Final Boss"))
                self.attack()
            else:
                print("The Final Boss is not near.......")

    def pickup_loot(self, monster: data.Monster) -> None:
        """Check if monster have loot and add it to the respective inventories"""
        if not monster.items:
            return
        for item_name in monster.items:
            item = data.get_item(item_name)
            if isinstance(item, data.HealthItem):
                self.player.healthitems.add(item)
            elif isinstance(item, data.KeyItem):
                self.player.keyitems.add(item)
            elif isinstance(item, data.Weapon):
                self.player.weapons.add(item)
            else:
                print(f"{item_name} not found, please report this error.")
                return
            print(f"+{item} added to your inventory!")
            self.display_status(item)

    def show_layout(self, slot: int)-> None:
        """Prints the attacking layout"""
        monster = data.get_monster(self.current_room.monster)
        divider = " |"
        spacer = ((slot*2+ 1 - 7)//2) *" "
        print("\n----------ATTACKING----------")
        print(f"{monster.name} HP: {monster.get_health()}")
        print("\t\t"+"_" * (slot*2 + 1))
        print(f"\t\t|{divider * slot}")
        print("\t\t" +" "+ " ".join([str(i) for i in range(1,slot +1)]))
        print("\n"*2)
        print("\t\t" + spacer + ("_" * (5)))
        print("\t\t" + spacer + f"|{divider * 2}")
        print("\t\t" + spacer + " "+ " ".join([str(i) for i in range(1,3)]))
        print(f"Your HP: {self.player.get_health()}")
        print("-"*30+"\n")

    def get_possible_actions(self) -> list[data.Action]:
        """Returns a list of possible Action objects"""
        copy_list = data.actionslist().copy()
        if self.current_room == data.get_room("Abandoned Staff Room"):
            copy_list.remove(data.ATTACK)
            return copy_list
        
        if not self.current_room.is_fully_visited():
            copy_list.remove(data.ATTACK)
            return copy_list
        else:
            monster = data.get_monster(self.current_room.monster)
            if monster and not monster.is_dead():
                self.display_status(monster)
                copy_list.remove(data.EXPLORE)
                copy_list.remove(data.GOTO_ROOM)
                return copy_list
            else:
                copy_list.remove(data.ATTACK)
                return copy_list
    
    def get_randomised_loot(self) -> None:
        """Adds randomised weapon into players inventory"""
        if self.current_room.visit_count <= 2:
            if random.randint(1,5) == 1:
                if random.randint(1,2) == 1:
                    found_item = data.healthitems[random.randint(0,len(data.healthitems)-1)]
                    self.player.healthitems.add(found_item)
                    print(f"You found {found_item.name}!!")
                    return found_item

        elif self.current_room.visit_count <= 4:
            if random.randint(1,2) == 1:
                if random.randint(1,2) == 1:
                    found_item = data.healthitems[random.randint(0,len(data.healthitems)-1)]
                    self.player.healthitems.add(found_item)
                    print(f"You found {found_item.name}!!")
                    return found_item


        elif self.current_room.visit_count > 5:
            if random.randint(1,2) == 1:
                if random.randint(1,2) == 1:
                    found_item = data.healthitems[random.randint(0,len(data.healthitems)-1)]
                    self.player.healthitems.add(found_item)
                    print(f"You found {found_item.name}!!")
                    return found_item
                    
    def prompt_valid_actions(self, possible_actions: list[data.Action]) -> data.Action:
        """Displays possible actions, gets user input and return the action object"""
        #Display and Get user input
        action = self.prompt(possible_actions, "WHAT DO YOU WANT TO DO?")
        #Return Action object
        return action

    def execute_action(self, action: data.Action) -> None:
        """Execute chosen action"""
        if action == data.EXPLORE:
            #Prints description of explore, randomise loot, and increments ec
            self.display_status(self.current_room)
            self.display_status(self.get_randomised_loot())
            self.current_room.visit()

        elif action == data.GOTO_ROOM:
            #change room and print room status
            self.move_to_room()
            self.display_status(self.current_room)
            self.current_room.visit()

        elif action == data.USE_ITEM:
            self.use_item()

        elif action == data.ATTACK:
            self.attack()
    
    def run(self) -> None:
        """Run the game loop"""
        #-----game loop--------
        #welcome message
        data.welcome()
        while not self.gameover:
            #Display action
            print("="*60)
            self.display_status(self.player)
            #Get possible actions
            possible_actions = self.get_possible_actions()
            #Get chosen action 
            action = self.prompt_valid_actions(possible_actions) 
            #Execute action
            self.execute_action(action)
            #Check if game over
            self.check_gameover()
            
