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
    return f"You guessed correctly and dealt {dmg} damage!"
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

def welcome() -> None:
    return "Welcome to a Post-Apocalyptic version of NYJC. After oppenheimer dropped the third bomb, Singapore was devastated. You desperately want your A-level results located in the NYJC Staff Room. You reach NYJC only to realise it has been partially destroyed by the explosions. The main gate is overun with mutant creatures, hence you need to enter through the only available entry, the sheltered court face entry system. You have to navigate a post-apocolyptic NYJC overuned with mutant creatures, collect weapons, pick up key items, and ultimately collect your 'A' level certificate from the final boss."

def win() -> None:
    return "As you clutched your 'A' level certificate, a rush of emotions sweeps you over. This piece of paper represented more than just your academic achievement; it symbolized your indomitable spirit, adaptability, and the unwavering commitment to your dreams even amidst the harshest of circumstances. Your journey through the post-apocalyptic school was not just a quest for a certificate, but a testament to the power of education and the human spirit. Congratulations player, you have beat the Final Boss and collected your 'A' levels certificate."

def loseboss() -> None:
    "With a heavy heart, you stand amidst the debris and shadows of the post-apocalyptic school, your quest to retrieve your 'A' level certificate from the clutches of the final boss having ended in defeat. Despite your long and arduous exploration, your efforts were not enough to overcome the challenges that awaited you within these decaying walls. As you gaze around the abandoned school, the weight of disappointment settles upon your shoulders. The corridors that once echoed with the laughter and footsteps of students now reverberate with the emptiness of a world forever changed. The final boss, a formidable adversary, had proven to be an insurmountable obstacle, guarding the precious certificates within the heart of this fallen institution. You lose."

def loseothers() -> None:
    "Unfortunately, your quest to retrieve your 'A' level certificate has ended and you have died. You recall the trials you faced – the treacherous journey through darkened classrooms, the tense encounters with remnants of security systems, and the labyrinthine corridors that seemed to shift and deceive. Each step you took was a testament to your determination, but alas, the odds were not in your favor this time. With a sigh, you realize that the certificate, a symbol of your achievements and hard work, remains beyond your grasp. You lose."