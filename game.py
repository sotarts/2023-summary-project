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
                   
    def prompt(self, options: list[str], question: str, show=True) -> str:
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
                print("That is not a valid input. Please enter again\n")
        print("")
        return userinput
                
    def move_to_room(self) -> None:
        """Prompts room and update current room based on input of the player"""
        room_names = data.room_names()
        room_names.remove("Abandoned Staff Room")
        room_name = self.prompt(room_names, "WHICH ROOM DO YOU WANT TO GO TO?")
        self.current_room = data.get_room(room_name)
  
    def attack(self) -> None:
        """WHOLE ATTACKING SEQUENCE, attacks monster in current room. """
        #---ATTACK LOOP---
        monster = data.get_monster(self.current_room.monster)
        while monster and not self.player.is_dead():
            self.show_layout(monster.slot)
            dodge_slot = self.prompt([1, 2], "You have a chance to dodge, which slot will you like to dodge to?", False)
            slot_list = []
            for i in range(1, monster.slot + 1):
                slot_list.append(i)

            attack_slot = self.prompt(slot_list,"Choose which square you would like to attack.", False)
            choice = self.prompt(self.player.weapons.contents(), "Which weapon do you want to use?")
            chosen_weapon = self.player.weapons.get(choice)

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
        item_type = self.prompt(["Health Items", "Key Items"], "WHICH TYPE OF OBJECT DO YOU WANT TO USE?")
        if item_type == "Health Items":                 
            if self.player.healthitems.is_empty():
                print("You do not have any health items")
                return
            choice = self.prompt(self.player.healthitems.contents(), "WHICH OBJECT DO YOU WANT TO USE?")
            healthitem = self.player.healthitems.get(choice)
            self.use_healthitem(healthitem)
            
        elif item_type == "Key Items":
            if self.player.keyitems.is_empty():
                print("You do not have any Key items")
                return
            choice = self.prompt(self.player.keyitems.contents(),"WHICH OBJECT DO YOU WANT TO USE?")
            keyitem = self.player.keyitems.get(choice)
            self.use_keyitem(keyitem)

    def use_healthitem(self, healthitem: data.HealthItem)-> None:
        """Updates the player health using the chosen item"""
        self.player.healthitems.remove(healthitem.name)
        self.player.update_health(healthitem.health)
        print(f"You used up 1 {healthitem.name} and healed {healthitem.health} HP!")

    def use_keyitem(self, keyitem: data.KeyItem) -> None:
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

    def get_possible_actions(self) -> list[str]:
        """Returns a list of possible Action objects"""
        actions = data.get_actions()
        if self.current_room == data.get_room("Abandoned Staff Room"):
            actions.remove(data.ATTACK)
            return actions
        
        if not self.current_room.is_fully_visited():
            actions.remove(data.ATTACK)
            return actions
        else:
            monster = data.get_monster(self.current_room.monster)
            if monster and not monster.is_dead():
                self.display_status(monster)
                actions.remove(data.EXPLORE)
                actions.remove(data.GOTO_ROOM)
                return actions
            else:
                actions.remove(data.ATTACK)
                return actions
    
    def get_randomised_loot(self) -> None:
        """Adds randomised weapon into players inventory"""
        if self.current_room.visit_count <= 2:
            if random.randint(1,5) == 1:
                if random.randint(1,2) == 1:
                    found_item = data.get_random_healthitem()
                    self.player.healthitems.add(found_item)
                    print(f"You found {found_item.name}!!")
                    return found_item

        elif self.current_room.visit_count <= 4:
            if random.randint(1,2) == 1:
                if random.randint(1,2) == 1:
                    found_item = data.get_random_healthitem()
                    self.player.healthitems.add(found_item)
                    print(f"You found {found_item.name}!!")
                    return found_item


        elif self.current_room.visit_count > 5:
            if random.randint(1,2) == 1:
                if random.randint(1,2) == 1:
                    found_item = data.get_random_healthitem()
                    self.player.healthitems.add(found_item)
                    print(f"You found {found_item.name}!!")
                    return found_item
                    
    def prompt_valid_actions(self, possible_actions: list[str]) -> str:
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
            
