def welcome() -> str:
    print( "Welcome to a Post-Apocalyptic version of NYJC. After oppenheimer dropped the third bomb, Singapore was devastated. You desperately want your A-level results located in the NYJC Staff Room. You reach NYJC only to realise it has been partially destroyed by the explosions. The main gate is overun with mutant creatures, hence you need to enter through the only available entry, the sheltered court face entry system. You have to navigate a post-apocolyptic NYJC overuned with mutant creatures, collect weapons, pick up key items, and ultimately collect your 'A' level certificate from the final boss. ")

def room_dict() -> dict:
    room_dict = { "Shuttle Courts": {
      "name": "Overgrown Shuttle Courts",
      "description": "Stepping outside, you find yourself in the overgrown shuttle courts swallowed by nature. Tall grasses and vines obscure the cracked pavement. The skeletal remains of the basketball hoop creak in the breeze. A sense of desolation hangs in the air."
    },
                 "Canteen": {"name": "Ransacked Canteen",
      "description": "You enter what used to be the canteen, now a scene of chaos. Tables and chairs are overturned, and the floor is littered with discarded wrappers and cans. A faint odor of spoiled food lingers."},
                      "Concourse": {"name": "Ruined Concoursed",
      "description": "A You stand amidst the crumbling pillars and shattered glass, the school's once vibrant concourse now lies in ruins. Faded CCA posters now cling to peeling walls, echoes of laughter replaced by eerie silence. The scent of dampness and decay fills the air."
    },
                  "Libary": {
      "name": "Forgotten Library",
      "description": "Rows of bookshelves stretch before you, their contents reduced to ruins by time and neglect. Sunlight filters through cracked windows, casting eerie shadows on the torn pages that flutter in the breeze. An air in the libary hangs heavily."
    },
                  "Staff Room": {
      "name": "Abandoned Staff Room",
      "description": "Before you stretches an empty room, its lights flickering as old worksheets are strewn all over the place. The wooden floor is warped and cracked. Faded words are left on the whiteboard, noting down abscence of teachers and important admin information. A strange silence pervades the space."
                  }}
    return room_dict
                  
                  
                  