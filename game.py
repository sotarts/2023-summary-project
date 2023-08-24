#Test move room works
#Test attack monster works (game ends when you die)
#Test monster drop works

import data
import random

class Game:
    def __init__(self)-> None:
        self.player = data.Player()
        self.gameover = False
        self.current_room = data.get_room("Overgrown Sheltered Courts")

    def show_status(self) -> None:
        """prints the health and the current room the player is in"""
        print(f"HEALTH: {self.player.get_health()}\nCURRENT ROOM: {self.current_room.name}")

    def attack_status(self, monster: object) -> None:
        """Prints the name and health of the monster and your health"""
        print(f"\nMonster hp: {monster.get_health()}\nYour hp: {self.player.get_health()}\n")

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
                   
    def prompt(self, data:list[object], question:str) -> object:
        """Takes in a list of object and a question, returns the chosen object"""
        for i in range(len(data)):
            print(f"{i+1}: {data[i].name}")

        userinput = None
        while not userinput:
            userinput = input(f"{question} (SELECT A NUMBER)  ")
            if userinput.isdecimal() and int(userinput) < len(data) + 1:
                print("")
                return data[int(userinput)-1]
                break
            else:
                userinput = None
                print("That is not a valid input. Please enter again\n")

    def prompt_non_obj(self, data: list, question:str):
        userinput = None
        while not userinput:
            userinput = input(f"{question} (SELECT A NUMBER)  ")
            if userinput.isdecimal() and int(userinput) < len(data) + 1:
                print("")
                return data[int(userinput)-1]
                break
            userinput = None
            print("That is not a valid input. Please enter again\n")
                
    def move_to_room(self) -> None:
        """Prompts room and update current room based on input of the player"""
        room = self.prompt(data.rooms, "WHICH ROOM DO YOU WANT TO GO TO?")
        self.current_room = room
        print("-"*20)
        print(self.current_room.description)
        print("-"*20)

    def attack(self) -> None:
        """WHOLE ATTACKING SEQUENCE """
        #---ATTACK LOOP---
        while self.current_room.monster and self.player.health > 0:
            self.show_layout(5)
            dodge_slot = self.prompt_non_obj([1,2,3],"You have a chance to dodge, which slot will you like to dodge to?")
            attack_slot = self.prompt_non_obj([1,2,3,4,5],"Choose which square you would like to attack.")
            chosen_weapon = self.prompt(data.weapons, "Which weapon do you want to use?")

            if attack_slot == random.randint(1,1):
                self.current_room.monster.update_health(self.player.ap * chosen_weapon.ap *-1)
                print(f"You guessed correctly and dealt {self.player.ap * chosen_weapon.ap} damage!")
            else:
                print("Oops, your attack missed the monster..")
                
            if self.current_room.monster.get_health() > 0:
                if random.randint(1,4) == dodge_slot:
                    self.player.update_health(self.current_room.monster.ap*-1)
                    print(f"Uh oh, you ran into the monster's attack path, you lost {self.current_room.monster.ap} HP..")

                else:
                    print("You managed to dodge the monsters attack successfully!")

            else:
                print("You have killed the monster!!!")
                self.current_room.monster_isdead()

    def use_item(self) -> None:
        item_type = self.prompt_non_obj(["Health Items", "Key Items"], "Which object do you want to use?")
        if item_type == "Health Item":                 
            self.use_healthitem(self.prompt(self.player.healthitems.get_inventory()))
            
        elif item_type == "Key Items":
            self.use_keyitem(self.prompt(self.player.keyitems.get_inventory()))

    def use_healthitem(self, healthitem: object)-> None:
        """Updates the player health using the chosen item"""
        self.player.update_health(healthitem.health)

    def pickup_loot(self) -> None:
        """Check if monster have loot and add it to the respective inventories"""
        if not self.current_room.monster.dropitem:
            if self.current_room.monster.dropitem.type() == "Health Items":
                self.player.healthitems.add
                pass
            
    def use_keyitem(self, keyitem:object) -> None:
        if keyitem == data.get_keyitem("Keycard"):
            if self.current_room == data.get_room("Forgotten Library"):
                self.current_room = data.get_room("Abandoned Staff Room")
                print("You have accessed the staff room... the final boss might be lurking nearby....")
            else:
                print("There is no use for this item in this room.")

                
    def show_layout(self, slot: int):
        divider = " |"
        spacer = ((slot*2+ 1 - 7)//2) *" "
        print("\n----------ATTACKING----------")
        print(f"{self.current_room.monster.name} HP: {self.current_room.monster.get_health()}")
        print("_" * (slot*2 + 1))
        print(f"|{divider * slot}")
        print(" "+ " ".join([str(i) for i in range(1,slot +1)]))
        print("\n"*2)
        print(spacer + ("_" * (7)))
        print(spacer + f"|{divider * 3}")
        print(spacer + " "+ " ".join([str(i) for i in range(1,4)]))
        print(f"Your HP: {self.player.get_health()}")
        print("-"*30+"\n")

    def get_possible_actions(self) -> list["Action"]:
        """Returns a list of possible Action objects"""
        if self.current_room.get_ec() <= 2:
            p_actions = data.actionslist()
            p_actions.remove(data.ATTACK)
            return p_actions

        else:
            if self.current_room.get_monster() != False:
                print(f"\nYou found the {self.current_room.monster.name}!\nDESCRIPTION: {self.current_room.monster.description}\n")
                p_actions = data.actionslist()
                p_actions.remove(data.EXPLORE)
                p_actions.remove(data.GOTO_ROOM)
                return p_actions

            else:
                p_actions = data.actionslist()
                p_actions.remove(data.ATTACK)
                return p_actions

    def prompt_valid_actions(self, possible_actions: list["Action"]) -> "Action":
        """Displays possible actions, gets user input and return the action object"""
        #Display and Get user input
        action = self.prompt(possible_actions, "WHAT DO YOU WANT TO DO?")
        #Return Action object
        return action

    def execute_action(self, action):
        """Execute chosen action"""
        if action == data.EXPLORE:
            print("You have explored the room")
            self.current_room.increment_ec()

        elif action == data.GOTO_ROOM:
            self.move_to_room()

        elif action == data.USE_ITEM:
            self.show_layout(3)
            pass

        elif action == data.ATTACK:
            self.attack()
            pass
    
    def run(self):
        #-----game loop--------
        #welcome message
        data.welcome()
        while not self.gameover:
            #Display action
            print("="*20)
            self.show_status()
            #Get possible actions
            possible_actions = self.get_possible_actions()
            #Get chosen action 
            action = self.prompt_valid_actions(possible_actions) 
            #Execute action
            self.execute_action(action)
            #Check if game over
            self.check_gameover()
