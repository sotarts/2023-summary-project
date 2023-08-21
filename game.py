#Test move room works
#Test attack monster works (game ends when you die)
#Test monster drop works

import data

class Game:
    def __init__(self):
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
            #self.lose()
            print("You died")
            self.gameover = True

        #elif finalmonster.health == 0:
        #    self.win()
        #    self.gameover = True
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
                return data[int(userinput)-1]
                break
            else:
                userinput = None
                print("That is not a valid input. Please enter again")
        
    def move_to_room(self) -> None:
        """Prompts room and update current room based on input of the player"""
        room = self.prompt(data.rooms, "WHICH ROOM DO YOU WANT TO GO TO?")
        self.current_room = room

    def attack(self) -> None:
        """WHOLE ATTACKING SEQUENCE """
        #---ATTACK LOOP---
        while self.current_room.monster.get_health() > 0 and self.player.health > 0:
            #Display monster and your status
            self.attack_status(self.current_room.monster)
            #Prompt and get what weapon they want to use
            chosen_weapon = self.prompt(data.weapons, "WHICH WEAPON DO YOU WANT TO USE?")
            #Deal the damage to the monster
            dealt_damage = self.player.ap * chosen_weapon.ap
            print(f"You dealt {dealt_damage} to {self.current_room.monster.name}.")
            self.current_room.monster.update_health(self.player.ap * chosen_weapon.ap * -1)
            #Check if monster or player is dead, exit loop if true
            if self.current_room.monster.get_health() <= 0:
                print(f"You have killed the {self.current_room.monster.name}")
                self.current_room.monster_isdead()
                break
            elif self.player.health <= 0:
                break
            #Monster deal its damage back
            self.player.update_health(self.current_room.monster.ap * -1)
            print(f"{self.current_room.monster.name} dealt {self.current_room.monster.ap} to you.")
            
    def get_possible_actions(self) -> list["Action"]:
        """Returns a list of possible Action objects"""
        if self.current_room.get_ec() <= 2:
            p_actions = data.actionslist()
            p_actions.remove(data.ATTACK)
            return p_actions

        else:
            if self.current_room.get_monster() != False: #ADD get_monster() method Room.monster = FALSE if dead
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
        
game = Game()
game.run()
    