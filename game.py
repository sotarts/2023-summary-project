import data

class Game:
    def __init__(self):
        self.player = data.Player()
        self.gameover = False
        self.current_room = data.get_room("Overgrown Sheltered Courts")

    def show_status(self) -> None:
        """prints the health and the current room the player is in"""
        print(f"HEALTH: {self.player.get_health()}\nCURRENT ROOM: {self.current_room.name}")
    
    def prompt(self, data:list[object], question:str) -> object:
        """Takes in a list of object and a question, returns the chosen object"""
        for i in range(len(data)):
            print(f"{i}: {data[i].name}")

        userinput = None
        while not userinput:
            userinput = input(f"{question} (SELECT A NUMBER)  ")
            if not userinput.isdecimal() and userinput < len(self.actionslist):
                continue
            else:
                print("That is not a valid input. Please enter again")

        return data[userinput]
        
    def move_to_room(self) -> None:
        """Prompts room and update current room based on input of the player"""
        room = self.prompt(data.get_room(), "WHICH ROOM DO YOU WANT TO GO TO?")
        self.current_room = room
            
    def get_possible_actions(self) -> list[Action]:
        """Returns a list of possible Action objects"""
        if self.current_room.get_monster() and self.current_room.get_ec() > 2: #ADD get_monster() method Room.monster = FALSE if dead
            p_actions = data.actionslist()
            p_actions.remove(data.EXPLORE)
            p_actions.remove(data.GOTO_ROOM)

        elif self.current_room.get_ec() <= 2:
            p_actions = data.actionslist()
            p_actions.remove(data.ATTACK)
             
        return p_actions
        
    def prompt_valid_actions(self, possible_actions: list[Action]) -> Action:
        """Displays possible actions, gets user input and return the action object"""
        #Display possible actions
        for i in range(len(possible_actions)):
            print(f"{i}: {possible_actions[i].name}")
        #Get user input
        action = self.prompt(possible_actions, "WHAT DO YOU WANT TO DO?")
        #Return Action object
        return action
    
    def execute_action(self, action):
        """Execute chosen action"""
        if action == data.EXPLORE:
            print("You have explored the room")
            self.current_room.increment_ec()

        elif action == data.GOTO_ROOM:
            self.current_room.move_to_room()
        pass

    def run(self):
        #-----game loop--------
        #welcome message
        data.welcome()
        while not self.gameover:
            #Display action
            self.show_status()
            #Get possible actions
            possible_actions = self.get_possible_actions()
            #Show valid actions 
            self.prompt_valid_actions(possible_actions)
        

    
    
    
    
        
        
            
    