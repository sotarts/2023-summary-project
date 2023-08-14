#imports
import random
import data


class Character:
    def __init__(self):
        pass

# Game
class Game:

    def __init__(self):
        self._gameover = False
        self.charname = None

        #instantiate player
        self.player = Character()

        #instantiate rooms
        self.rooms = []

    def create_rooms(self) -> None:
        pass

    def display_status(self) -> None:
        pass

    def game_is_over(self) -> bool:
        return self._gameover

    def get_character_name(self) -> None:
        """Gets users character name and returns the name chosen"""
    
        self.charname = input("What will be your name?: ")
        reply = input(f'You will be {self.charname} from class of 2024, do you wish to change your name? (y/n)   ')

        #change name loop
        while reply.upper() != 'N':
            print("\n")
            self.charname = input("What will be your new name then?: ")
            reply = input(f'You will be {self.charname} from class of 2024, do you wish to change your name again? (y/n)   ')

    def show_actions(self, explored_counter) -> None: #ask wanqi to add explored counter attribute for each room
        if explored_counter:
            pass

    def get_user_input(self) -> int: #integer will be used to choose the options
        pass

    def execute_action(self, index: int) -> None:
        pass
  
    def run_game(self):
        #show welcome message
        print("WElCOME...........") # function welcome() -> None: needed
        #allow user to set character name and stores character name
        self.get_character_name()
        print("<<situation>>") # function scenario() -> None: needed

        # INSTANTIATE OBJ
        player = Character
        #LOOP START
        while self._gameover is not True:
            #SHOW STATUS
            self.display_status()
            #SHOW POSSIBLE ACTIONS
            self.show_actions() #room.explored counter needed
            #EXECUTE ACTION
            self.execute_action()
            #UPDATE DATA
            self.update_data()
            #CHECK GAME_OVER
            self.check_gameover()

