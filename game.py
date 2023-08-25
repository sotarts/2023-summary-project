#Test move room works
#Test attack monster works (game ends when you die)
#Test monster drop works

import data
import random

class Game:
    """Encapsulates the main game"""
    def __init__(self)-> None:
        self.player = data.Player()
        self.gameover = False
        self.current_room = data.get_room("Overgrown Sheltered Courts")

        # Add first weapon; fists into the weapons inventory
        self.player.weapons.add(data.get_weapon("Chemical Thrower"))

    def display_status(self, obj: object, incremented_desc=False) -> None:
        """Takes in any object and print the relevant info based on what type the object is."""
        if not obj:
            return
        if isinstance(obj, data.Player):
            print(f"HEALTH: {self.player.get_health()}\nCURRENT ROOM: {self.current_room.name}")

        elif isinstance(obj, data.Room):
            if incremented_desc:
                print("-----EXPLORED RESULTS-----")
                if obj.get_ec() < obj.max_explored:
                    print(obj.description[obj.get_ec()])
                    print("")
                    pass
                else:
                    print("There is nothing left to explore.\n")
            else:
                print(("-"*5) + obj.name + ("-"*5) )
                print(f"DESCRIPTION: {obj.description}")

        elif isinstance(obj, data.Monster):
            print(f"\nYou found the {self.current_room.monster.name}!\nDESCRIPTION: {self.current_room.monster.description}\n")

        elif isinstance(obj, data.Weapon):
            print(("-"*5) + obj.name + "'s Status" + ("-"*5) )
            print(f"DESCRIPTION: {obj.description}\nATTACK BUFF: +{obj.ap}")

        elif obj.category == "key_item":
            print(("-"*5) + obj.name + "'s Status" + ("-"*5) )
            print(f"DESCRIPTION: {obj.description}\nUSAGE:{obj.usage}")

        elif obj.category == "health_item":
            print(("-"*5) + obj.name + "'s Status" + ("-"*5) )
            print(f"DESCRIPTION: {obj.description}\nHEALTH:{obj.health}")

    def check_gameover(self) -> None:
        """Check if game is over, if the player win, win method is called, while if player lose, losing method is called BOTH is asked to restart"""
        if self.player.health <= 0:
            print("You died................")
            self.gameover = True

        elif data.get_monster("Final Boss").get_health() <= 0:
            print("You have succesfully killed the final boss and won the game!!!! Hooray!!\nAs you watch the final boss turn into  dust you realised you didnt actually take Alevels but took IB instead :)")
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
            userinput = input(f"{question} (SELECT A NUMBER)  ")
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
        while self.current_room.monster and self.player.health > 0:
            self.show_layout(self.current_room.monster.slot)
            dodge_slot = self.prompt([1,2],"You have a chance to dodge, which slot will you like to dodge to?", False, False)
            slot_list = []
            for i in range(1,self.current_room.monster.slot +1):
                slot_list.append(i)

            attack_slot = self.prompt(slot_list,"Choose which square you would like to attack.", False, False)
            chosen_weapon = self.prompt(self.player.weapons.get_inventory(), "Which weapon do you want to use?")

            print("-----BATTLE RESULT-----")
            if attack_slot == random.randint(1,self.current_room.monster.slot): #change b to max slot of monster
                self.current_room.monster.update_health(self.player.ap * chosen_weapon.ap *-1)
                print(f"You guessed correctly and dealt {self.player.ap * chosen_weapon.ap} damage!")
            else:
                print("Oops, your attack missed the monster..")
                
            if self.current_room.monster.get_health() > 0:
                if random.randint(1,4) == dodge_slot:
                    self.player.update_health(self.current_room.monster.ap*-1)
                    print(f"Uh oh, you ran into the monster's attack path, you lost {self.current_room.monster.ap} HP..")
                else:
                    print("You managed to dodge the monsters attack successfully!\n")
            else:
                print("You have killed the monster!!!\n")
                print("-----SPOILS-----")
                self.pickup_loot(self.current_room.monster)
                self.current_room.monster_isdead()
                
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

    def pickup_loot(self, monster: object) -> None:
        """Check if monster have loot and add it to the respective inventories"""
        if not monster.item:
            return
        for i in range(len(monster.item)):
            if monster.item[i].category == "health_item":
                self.player.healthitems.add(monster.item[i])
                
            elif monster.item[i].category == "key_item":
                self.player.keyitems.add(monster.item[i])

            elif monster.item[i].category == "weapons":
                self.player.weapons.add(monster.item[i])
                
            print(f"+{self.current_room.monster.item[i].name} added to your inventory!")
            self.display_status(monster.item[i])

    def show_layout(self, slot: int)-> None:
        """Prints the attacking layout"""
        divider = " |"
        spacer = ((slot*2+ 1 - 7)//2) *" "
        print("\n----------ATTACKING----------")
        print(f"{self.current_room.monster.name} HP: {self.current_room.monster.get_health()}")
        print("\t\t"+"_" * (slot*2 + 1))
        print(f"\t\t|{divider * slot}")
        print("\t\t" +" "+ " ".join([str(i) for i in range(1,slot +1)]))
        print("\n"*2)
        print("\t\t" + spacer + ("_" * (5)))
        print("\t\t" + spacer + f"|{divider * 2}")
        print("\t\t" + spacer + " "+ " ".join([str(i) for i in range(1,3)]))
        print(f"Your HP: {self.player.get_health()}")
        print("-"*30+"\n")

    def get_possible_actions(self) -> list["Action"]:
        """Returns a list of possible Action objects"""
        copy_list = data.actionslist().copy()
        if self.current_room == data.get_room("Abandoned Staff Room"):
            copy_list.remove(data.ATTACK)
            return copy_list
        
        if self.current_room.get_ec() <= self.current_room.max_explored:
            copy_list.remove(data.ATTACK)
            return copy_list
        else:
            if self.current_room.get_monster() != False:
                self.display_status(self.current_room.monster)
                copy_list.remove(data.EXPLORE)
                copy_list.remove(data.GOTO_ROOM)
                return copy_list
            else:
                copy_list.remove(data.ATTACK)
                return copy_list
    
    def get_randomised_loot(self) -> None:
        """Adds randomised weapon into players inventory"""
        if self.current_room.get_ec() <= 2:
            if random.randint(1,5) == 1:
                if random.randint(1,2) == 1:
                    found_item = data.healthitems[random.randint(0,len(data.healthitems)-1)]
                    self.player.healthitems.add(found_item)
                    print(f"You found {found_item.name}!!")
                    return found_item

        elif self.current_room.get_ec() <= 4:
            if random.randint(1,2) == 1:
                if random.randint(1,2) == 1:
                    found_item = data.healthitems[random.randint(0,len(data.healthitems)-1)]
                    self.player.healthitems.add(found_item)
                    print(f"You found {found_item.name}!!")
                    return found_item


        elif self.current_room.get_ec() > 5:
            if random.randint(1,2) == 1:
                if random.randint(1,2) == 1:
                    found_item = data.healthitems[random.randint(0,len(data.healthitems)-1)]
                    self.player.healthitems.add(found_item)
                    print(f"You found {found_item.name}!!")
                    return found_item
                    
    def prompt_valid_actions(self, possible_actions: list["Action"]) -> "Action":
        """Displays possible actions, gets user input and return the action object"""
        #Display and Get user input
        action = self.prompt(possible_actions, "WHAT DO YOU WANT TO DO?")
        #Return Action object
        return action

    def execute_action(self, action: "Action") -> None:
        """Execute chosen action"""
        if action == data.EXPLORE:
            #Prints description of explore, randomise loot, and increments ec
            self.display_status(self.current_room, True)
            self.display_status(self.get_randomised_loot())
            self.current_room.increment_ec()

        elif action == data.GOTO_ROOM:
            #change room and print room status
            self.move_to_room()
            self.display_status(self.current_room, True)

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
            
