DIVIDER_CHAR = "="

def divider(width: int) -> str:
    return DIVIDER_CHAR * width

def header(title: str, width: int) -> str:
    """return a formatted header

    Example: ----- TITLE -----
    """
    assert width >= len(title) + 2
    side_len = (width - len(title) - 2) // 2
    return f"{'-' * side_len} {title} {'-' * side_len}"

input_invalid = "That is not a valid input. Please enter again"

prompt_action = "WHAT DO YOU WANT TO DO?"

prompt_room = "WHICH ROOM DO YOU WANT TO GO TO?"

prompt_dodge = "You have a chance to dodge, which slot will you like to dodge to?"

prompt_square = "Choose which square you would like to attack."

prompt_weapon = "Which weapon do you want to use?"

prompt_use_type = "WHICH TYPE OF OBJECT DO YOU WANT TO USE?"

prompt_use_item = "WHICH OBJECT DO YOU WANT TO USE?"

def attack_success(dmg: int) -> str:
    return f"You guessed correctly and dealt {self.player.ap * chosen_weapon.ap} damage!"
attack_fail = "Oops, your attack missed the monster.."

dodge_success = "You managed to dodge the monsters attack successfully!"
def dodge_fail(dmg: int) -> str:
    return f"Uh oh, you ran into the monster's attack path, you lost {dmg} HP..."

monster_killed = "You have killed the monster!!!"

def items_empty(itemtype: str) -> str:
    return f"You do not have any {itemtype}"

def use_item(item_name: str, effect: str) -> str:
    return f"You used {item_name} and {effect}!"

def found_item(item_name: str) -> str:
    return f"You found {item_name}!!"

use_boss_key = "You have accessed the staff room... the Final Boss might be lurking nearby...."
use_wrong_key = "There is no use for this item in this room. Perhaps you should go to a different room....."

boss_encounter = "You summoned the Final Boss....."
no_boss_encounter = "The Final Boss is not near......."

def item_error(name: str) -> str:
    return f"{name} not found, please report this error."

def take_item(name: str) -> str:
    return f"+{name} added to your inventory!"