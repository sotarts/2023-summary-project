#imports
import random
import data


# Game
class Game:
    def __init__(self, roomdict):
        self.player = data.Player()
        self.actionslist = data.actionslist()
        self.gameover = False
        self.allrooms = roomdict
        self.current_room = self.allrooms["a"]

    def move_to_room(self, chosen_room: str) -> None:
        """Change and update current room based on the input of the player"""
        if chosen_room in self.allrooms:
            self.current_room = self.allrooms[chosen_room]
        else:
            print("room does not exist")

    def show_status(self) -> None:
        """Prints the health and attack power of the player"""
        print(
            f"HEALTH: {self.player.health}\nATTACK POWER: {self.player.ap}\nCURRENT ROOM: {self.current_room}"
        )

    def possible_actions(self) -> list[str]:
        """Returns a list of possible actions based on certain criterias"""
        return self.actionslist

    def display_actions(self, possible_actionslist: list) -> None:
        """Display possible actions with index"""
        for count, action in enumerate(possible_actionslist):
            print(str(count) + ":", action)

    def get_action_input(self, possible_actionslist) -> int:
        """Gets the user input and returns the index of the input in the possible actions lists"""
        #NEED TO VALIDATE USER INPUT (WILL ADD LATER)
        userinput = int(
            input('WHAT DO YOU WANT TO DO? (SELECT THE NUMBER):  '))
        return self.actionslist.index(possible_actionslist[userinput])

    def get_room_input(self) -> str:
        return input('WHICH ROOM DO YOU WANT TO MOVE TO?:  ')

    def execute_action(self, chosen_action_index: int) -> None:
        """Execute the action """
        if chosen_action_index == 0:
            print("You have explored the room")

        elif chosen_action_index == 1:
            self.move_to_room(self.get_room_input())

    def run(self):
        #GAME LOOP
        while self.gameover is not True:
            #SHOW STATUS OF THE PLAYER
            self.show_status()
            #SHOW THE POSSIBLE ACTIONS
            self.display_actions(self.possible_actions())
            #GET USER INPUT
            user_input = self.get_action_input(self.possible_actions())
            self.execute_action(user_input)



game = Game(room_dict)
game.run()