
import streamlit as st
from engine.generate import text_generation as text
from engine.generate import image_generation as image
from engine.client import fal

if "history" not in st.session_state:
    st.session_state.history = text.get_guide_history()

if "second_run" not in st.session_state:
    st.session_state.second_run = False

def get_placeholder_image():
    from PIL import Image
    return Image.open("wait.png")

def get_spinner(image):
    from PIL import Image

    background = image
    overlay = Image.open("wait.png")

    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")

    new_img = Image.blend(background, overlay, 0.5)
    return new_img

@st.dialog("Load Game")
def load_game():
    file = st.file_uploader("Load Game", accept_multiple_files=False)

    if file:
        try:
            from cryptography.fernet import Fernet
            import os
            key = str.encode(os.getenv("ENCRYPTION_KEY"))
            cipher_suite = Fernet(key)

            bytes_data = file.getvalue()

            story = bytes_data[0:bytes_data.find(b"/"*20)]
            logic = bytes_data[bytes_data.find(b"/"*20) + 20:bytes_data.find(b"\\"*20)]
            history = bytes_data[bytes_data.find(b"\\"*20) + 20:len(bytes_data)]
            
            decoded_story = cipher_suite.decrypt(story)
            decoded_logic = cipher_suite.decrypt(logic)
            decoded_history = cipher_suite.decrypt(history)
            st.write(decoded_history)
            import ast
            lst = ast.literal_eval(str(decoded_history.decode("utf-8")))
            st.session_state.history = lst
            st.session_state.story = decoded_story.decode("utf-8")
            st.session_state.logic = decoded_logic.decode("utf-8")
        except:
            st.error("Could not load game.")
        else:
            st.rerun()

def save_game():
    from cryptography.fernet import Fernet
    import os
    key = str.encode(os.getenv("ENCRYPTION_KEY"))
    cipher_suite = Fernet(key)
    encoded_story = cipher_suite.encrypt(str.encode(str(st.session_state.story)))
    cipher_suite = Fernet(key)
    encoded_logic = cipher_suite.encrypt(str.encode(str(st.session_state.logic)))
    cipher_suite = Fernet(key)
    encoded_history = cipher_suite.encrypt(str.encode(str(st.session_state.history)))
    saved_game = encoded_story + b"/"*20 + encoded_logic + b"\\"*20 + encoded_history
    return saved_game

def start():
    st.session_state.history.append(
        {
            "role": "user",
            "parts": [
                "Start",
            ],
        }
    )
    return text.generate_response("Start", st.session_state.history, st.session_state.logic)

if "play" not in st.session_state:
    st.title("AI-Powered Text-Based Adventure")
    if st.button("Play game", use_container_width=True):
        st.session_state.play = True
        st.rerun()
else:
    if "image" not in st.session_state:
        st.session_state.image = get_placeholder_image()
    if "story" not in st.session_state and "logic" not in st.session_state:
        st.session_state.first_run = True
        generator = None
        progress_bar = st.empty()
        with progress_bar.container():
            st.progress(0)
        with st.status("Starting a new game..."):
            st.write("Writing story...")
            # st.session_state.story = text.generate_story()
            st.session_state.story = """World description:
Setting: Vast desert landscapes, shifting dunes, and ancient ruins. Lush oasis settlements with intricate irrigation systems. Scraps of old technology scattered everywhere, hinting at a forgotten past. The night sky reveals stars, and a distant, almost forgotten, space era.
Rules: Water is scarce; technology is unreliable, particularly in extreme desert conditions. Cars require constant maintenance and fuel. Trust is a rare commodity; diplomacy and combat are both viable options. Ancient Egyptian artifacts are dangerous.
Factions: Nomadic tribes roam the desert, fiercely independent, some embrace technology for survival. Oasis dwellers, more settled, control resources, trade routes. A secretive group seeks lost Egyptian tech, potentially dangerous.
NPCs: Ahmad, a skilled nomad mechanic, wary of outsiders. Kamal, an oasis elder, wise but cautious. Dr. Nasir, a mysterious Egyptian tech researcher, driven by ambition. Tariq, a car racer, always looking for a challenge.
Plot Hooks: A crashed space object is discovered near an oasis, its technology sparking conflict. Rumors of a hidden Egyptian vault beneath the sands surface. A valuable car part is stolen, leading to a desert chase. The Nomads are facing a water shortage, and the oasis is not sharing.
Story: Centuries ago, a technologically advanced Egyptian civilization vanished, leaving behind remnants of its power. Now, Nomads and Oasis dwellers struggle to survive in the harsh Desert, while the echoes of a Space-faring past stir beneath the sands. Ancient technology is being rediscovered, and its power could reshape the world, for better or worse.
Objective: Uncover the secrets of ancient Egyptian technology hidden within the desert, using your skills and your car to navigate treacherous terrain. Decide whether to share your findings with the nomads or the oasis dwellers, or keep them for yourself."""
            if st.session_state.second_run:
                st.session_state.story = """World description:
Setting: A vast space dotted with planets; ancient observatories built from massive stone structures; ruined cities on forgotten worlds; swirling nebula clouds and asteroid belts; a sense of cosmic mystery.
Rules: Travel between planets requires navigating asteroid fields; activating observatory mechanisms needs specific stone sequences; ancient texts hold clues to celestial events; time progresses with planetary cycles.
Factions: The Cartographers, obsessed with mapping the stars; the Stonekeepers, guardians of ancient observatories; the Wanderers, explorers seeking lost knowledge. Tensions exist over control of ancient sites.
NPCs: Anya, a Cartographer, eager to chart new planets; Kaelen, a Stonekeeper, wary of outsiders; Jax, a Wanderer, cryptic with hidden motives.
Plot Hooks: A strange energy pulse from a distant planet; ancient stone carvings reveal a hidden prophecy; a damaged observatory reveals a star chart with missing planets.
Story: An ancient observatory, built by a forgotten civilization using stone, holds the key to understanding the planets and preventing a coming cosmic alignment that threatens to destabilize space itself. The player must unravel the secrets of the observatory and its builders to save the solar system.
Objective: Discover the true purpose of the ancient observatory and its connection to the planets, preventing a catastrophic celestial event."""
            with progress_bar.container():
                st.progress(20)
            st.write("Building world...")
            # st.session_state.logic = text.generate_game_logic(st.session_state.story)
            st.session_state.logic = """```json
{
  "gameTitle": "Desert Echoes",
  "setting": "Vast desert landscapes with oasis settlements and ancient ruins. Scraps of forgotten technology are scattered throughout.",
  "rules": [
    "Water is scarce and essential for survival.",
    "Technology is unreliable, especially in extreme desert conditions.",
    "Vehicles require regular maintenance and fuel.",
    "Diplomacy and resourcefulness are key to overcoming challenges."
  ],
  "areas": [
    {
      "areaId": "desert_dunes",
      "name": "Desert Dunes",
      "description": "Endless waves of sand stretch in every direction. The sun beats down relentlessly. Your vehicle is essential for navigation.",
      "objects": [
        {"objectId": "player_car", "name": "Your Vehicle", "description": "A sturdy vehicle, your lifeline in the desert. Requires fuel and maintenance.", "isInteractive": false},
        {"objectId": "tech_scrap_1", "name": "Scrap Metal", "description": "A piece of rusted metal, possibly from old technology. Might be useful for repairs.", "isInteractive": true, "isCollectable": true},
        {"objectId": "sand_dune_obstacle", "name": "High Dune", "description": "A towering sand dune blocking your path. You'll need to find a way around.", "isInteractive": false}
      ],
      "exits": [{"areaId": "oasis_settlement", "direction": "east"}, {"areaId": "ancient_ruins_entrance", "direction": "north", "requiresItem": "map_fragment"}]
    },
    {
      "areaId": "oasis_settlement",
      "name": "Oasis Settlement",
      "description": "A lush oasis, a welcome sight in the harsh desert. Palm trees provide shade, and water flows freely. People are going about their day.",
      "objects": [
        {"objectId": "water_well", "name": "Water Well", "description": "A source of fresh water. Essential for survival.", "isInteractive": true, "interaction": "refill_water"},
        {"objectId": "market_stall_1", "name": "Market Stall", "description": "A stall selling various goods. You might find useful supplies here.", "isInteractive": true, "interaction": "trade"},
        {"objectId": "workshop_ahmad", "name": "Ahmad's Workshop", "description": "A workshop filled with tools and vehicle parts. Ahmad, a skilled mechanic, works here.", "isInteractive": true, "npcId": "ahmad"}
      ],
      "npcs": ["ahmad", "kamal"],
      "exits": [{"areaId": "desert_dunes", "direction": "west"}]
    },
    {
      "areaId": "ancient_ruins_entrance",
      "name": "Ruins Entrance",
      "description": "The entrance to ancient ruins, partially buried in the sand.  A sense of mystery hangs in the air.",
      "objects": [
        {"objectId": "ruined_wall_1", "name": "Collapsed Wall", "description": "A section of wall that has crumbled over time.", "isInteractive": false},
        {"objectId": "locked_door_ruins", "name": "Ancient Door", "description": "A heavy stone door, sealed shut. It looks like it requires a key.", "isInteractive": true, "isLocked": true, "requiredItem": "ancient_key"}
      ],
      "exits": [{"areaId": "desert_dunes", "direction": "south"}, {"areaId": "ruins_inner_chamber", "direction": "east", "requiresItem": "ancient_key"}]
    },
    {
      "areaId": "ruins_inner_chamber",
      "name": "Ruins Inner Chamber",
      "description": "The inner chamber of the ruins. Hieroglyphs cover the walls, and strange symbols are etched into the floor.",
      "objects": [
        {"objectId": "hieroglyph_wall_1", "name": "Hieroglyph Wall", "description": "A wall covered in ancient hieroglyphs. They might contain clues.", "isInteractive": true, "interaction": "examine_hieroglyphs"},
        {"objectId": "pedestal_1", "name": "Stone Pedestal", "description": "A stone pedestal with a recess on top. It looks like something is missing.", "isInteractive": true, "interaction": "place_artifact", "requiresItem": "ancient_artifact"}
      ],
      "exits": [{"areaId": "ancient_ruins_entrance", "direction": "west"}, {"areaId": "hidden_vault", "direction": "deeper", "requiresPuzzleSolved": "pedestal_puzzle"}]
    },
    {
      "areaId": "hidden_vault",
      "name": "Hidden Vault",
      "description": "A hidden vault deep within the ruins. Ancient technology hums with latent power.  This is the heart of the ancient civilization.",
      "objects": [
        {"objectId": "ancient_console_1", "name": "Ancient Console", "description": "A complex console with glowing symbols and buttons. It seems to control something important.", "isInteractive": true, "interaction": "activate_console", "requiresItem": "tech_tool"},
        {"objectId": "storage_container_1", "name": "Sealed Container", "description": "A large container, sealed with ancient mechanisms. It might hold valuable items.", "isInteractive": true, "interaction": "open_container", "requiresPuzzleSolved": "console_puzzle"}
      ],
      "exits": [{"areaId": "ruins_inner_chamber", "direction": "exit"}]
    }
  ],
  "npcs": [
    {
      "npcId": "ahmad",
      "name": "Ahmad",
      "location": "oasis_settlement",
      "role": "Mechanic",
      "dialogue": {
        "greeting": "Welcome to the oasis. Need vehicle repairs or parts?",
        "services": "I can repair your vehicle and trade vehicle parts. What do you need?",
        "rumors": "I've heard whispers of strange things in the desert ruins to the north... ancient tech, they say."
      }
    },
    {
      "npcId": "kamal",
      "name": "Kamal",
      "location": "oasis_settlement",
      "role": "Oasis Elder",
      "dialogue": {
        "greeting": "Peace be upon you, traveler. What brings you to our oasis?",
        "advice": "The desert is unforgiving. Seek knowledge, but be wary of its power.",
        "quest_hint": "An old map fragment in the dunes might guide you to forgotten places."
      }
    }
    /* Removed Dr. Nasir and Tariq to keep it simple and focused on core logic. Can be added later if needed, ensuring compliance. */
  ],
  "items": [
    {
      "itemId": "water_canteen",
      "name": "Water Canteen",
      "description": "A container for carrying water. Essential for desert travel.",
      "isUsable": true,
      "useAction": "drink_water",
      "startingItem": true
    },
    {
      "itemId": "map_fragment",
      "name": "Map Fragment",
      "description": "A tattered piece of an old map. It seems to show a location to the north.",
      "isKeyItem": true,
      "location": "desert_dunes",
      "locationDetails": "Found near a broken vehicle wreck in the Desert Dunes."
    },
    {
      "itemId": "ancient_key",
      "name": "Ancient Key",
      "description": "A heavy key made of an unknown metal, adorned with strange symbols. It looks like it could open an ancient door.",
      "isKeyItem": true,
      "location": "ruins_inner_chamber",
      "locationDetails": "Reward for examining the Hieroglyph Wall and solving a simple riddle (not explicitly defined here, can be added as a puzzle)."
    },
    {
      "itemId": "ancient_artifact",
      "name": "Ancient Artifact",
      "description": "A small, intricately carved artifact. It radiates a faint energy.",
      "isKeyItem": true,
      "location": "ruins_inner_chamber",
      "locationDetails": "Found in a hidden compartment after examining the Hieroglyph Wall."
    },
    {
      "itemId": "tech_tool",
      "name": "Tech Tool",
      "description": "A specialized tool for interacting with ancient technology.",
      "isKeyItem": true,
      "location": "oasis_settlement",
      "locationDetails": "Can be purchased from Ahmad in exchange for scrap metal."
    },
    {
      "itemId": "vehicle_part_engine",
      "name": "Engine Part",
      "description": "A spare engine part for your vehicle.",
      "isUsable": true,
      "useAction": "repair_vehicle",
      "location": "oasis_settlement",
      "locationDetails": "Can be traded from Ahmad or found in desert scraps."
    },
    {
      "itemId": "fuel_can",
      "name": "Fuel Can",
      "description": "A can of fuel for your vehicle.",
      "isUsable": true,
      "useAction": "refuel_vehicle",
      "location": "oasis_settlement",
      "locationDetails": "Can be purchased at the market stall."
    }
  ],
  "puzzles": [
    {
      "puzzleId": "pedestal_puzzle",
      "location": "ruins_inner_chamber",
      "type": "item_placement",
      "description": "Place the correct artifact on the pedestal.",
      "solutionItem": "ancient_artifact",
      "reward": "Opens passage to Hidden Vault"
    },
    {
      "puzzleId": "console_puzzle",
      "location": "hidden_vault",
      "type": "tech_activation",
      "description": "Activate the ancient console using the tech tool.",
      "requiredItem": "tech_tool",
      "solution": "Activate the console by using the tech tool and selecting the correct sequence of symbols (not explicitly defined, can be added as a mini-game).",
      "reward": "Opens the Sealed Container"
    }
    /* Removed Hieroglyph riddle puzzle for ancient key to keep it simple. Can be added later. */
  ],
  "progression": [
    "Start in Desert Dunes with basic supplies.",
    "Find Map Fragment in Desert Dunes.",
    "Reach Oasis Settlement using the map.",
    "Gather information and supplies in Oasis.",
    "Use Map Fragment to locate Ruins Entrance.",
    "Find Ancient Key (through interaction with Hieroglyphs - simplified to item location for now).",
    "Enter Ruins Inner Chamber using Ancient Key.",
    "Solve Pedestal Puzzle using Ancient Artifact.",
    "Enter Hidden Vault.",
    "Solve Console Puzzle using Tech Tool.",
    "Open Sealed Container and uncover ancient secrets.",
    "Game objective complete upon uncovering secrets."
  ],
  "stateTracking": {
    "playerInventory": [],
    "playerLocation": "desert_dunes",
    "vehicleFuel": 100,
    "vehicleHealth": 100,
    "puzzlesSolved": {"pedestal_puzzle": false, "console_puzzle": false}
  },
  "winConditions": ["Uncover the secrets of the Hidden Vault."],
  "loseConditions": ["Running out of water in the desert.", "Vehicle breakdown without repair in a remote area (simplified for now)."]
}
```"""
            if st.session_state.second_run:
                st.session_state.logic = """```json
{
  "game_logic": {
    "levels": [
      {
        "area_id": "observatory_entrance",
        "description": "The entrance to the ancient observatory. Massive iron doors are set into the mountainside.",
        "objects": [
          {"object_id": "iron_door", "description": "A massive iron door with no markings.", "interaction": "examine", "details": "The door is sealed shut."}
        ],
        "npcs": [
          {"npc_id": "kaelen", "name": "Kaelen", "description": "A Stonekeeper, guarding the entrance.", "dialogue": "Welcome, traveler. This observatory holds secrets best left undisturbed, but perhaps you are different. Prove your intentions are aligned with preservation, not disruption."}
        ],
        "transitions": {
          "north": "observatory_main_chamber"
        }
      },
      {
        "area_id": "observatory_main_chamber",
        "description": "The central chamber of the observatory. A large stone pedestal stands in the middle.",
        "objects": [
          {"object_id": "stone_pedestal", "description": "A tall stone pedestal with slots for stones.", "interaction": "examine", "details": "The pedestal has several empty slots, seemingly designed to hold specific stones in a sequence."},
          {"object_id": "stone_tablet", "description": "A stone tablet resting against a wall.", "interaction": "read", "details": "Ancient carvings cover the tablet. They depict celestial patterns and a sequence of symbols."}
        ],
        "npcs": [
          {"npc_id": "anya", "name": "Anya", "description": "A Cartographer, studying the chamber.", "dialogue": "These carvings... they speak of planetary alignments. I believe the pedestal is key to understanding them."}
        ],
        "transitions": {
          "south": "observatory_entrance",
          "east": "stonekeeper_sanctum",
          "west": "ancient_library"
        }
      },
      {
        "area_id": "stonekeeper_sanctum",
        "description": "A secluded chamber, seemingly used by the Stonekeepers.",
        "objects": [
          {"object_id": "stone_chest", "description": "A sturdy stone chest.", "interaction": "open", "details": "The chest is locked, but after some effort, it opens, revealing a set of carved stones."},
          {"object_id": "carved_stones", "description": "A set of carved stones with unique symbols.", "interaction": "take", "details": "These stones seem to match the slots on the pedestal in the main chamber.", "item_id": "stone_sequence"}
        ],
        "npcs": [],
        "transitions": {
          "west": "observatory_main_chamber"
        }
      },
      {
        "area_id": "ancient_library",
        "description": "Shelves carved into the stone walls hold ancient texts and scrolls.",
        "objects": [
          {"object_id": "ancient_text", "description": "A large, bound text filled with astronomical charts and writings.", "interaction": "read", "details": "The text details celestial mechanics and mentions a 'cosmic alignment'. Deciphering it reveals a sequence related to star positions.", "item_id": "decoded_text"}
        ],
        "npcs": [
          {"npc_id": "jax", "name": "Jax", "description": "A Wanderer, examining the texts.", "dialogue": "The stars whisper secrets to those who listen. This library holds echoes of forgotten knowledge, knowledge that could change everything."}
        ],
        "transitions": {
          "east": "observatory_main_chamber",
          "north": "planetary_observation_deck"
        }
      },
      {
        "area_id": "planetary_observation_deck",
        "description": "A platform overlooking a vast expanse of space. A complex console stands here.",
        "objects": [
          {"object_id": "star_chart_console", "description": "A console with intricate controls and a holographic display showing star charts.", "interaction": "use", "details": "The console seems to require a specific star alignment to activate."},
          {"object_id": "observatory_mechanism", "description": "A large, intricate mechanism built into the platform.", "interaction": "examine", "details": "This mechanism appears to control the observatory's core functions, but it is currently inactive."}
        ],
        "npcs": [],
        "transitions": {
          "south": "ancient_library",
          "east": "asteroid_field_transition"
        }
      },
      {
        "area_id": "asteroid_field_transition",
        "description": "A dangerous asteroid field, the path to distant planets.",
        "objects": [],
        "npcs": [],
        "transitions": {
          "west": "planetary_observation_deck",
          "east": "distant_planet"
        }
      },
      {
        "area_id": "distant_planet",
        "description": "A distant planet, the destination revealed by the observatory.",
        "objects": [],
        "npcs": [],
        "transitions": {}
      }
    ],
    "items": [
      {"item_id": "stone_sequence", "name": "Carved Stones", "description": "A set of stones carved with symbols, fitting for the pedestal.", "usable": true, "use_location": "observatory_main_chamber", "use_object": "stone_pedestal"},
      {"item_id": "decoded_text", "name": "Decoded Text", "description": "A deciphered text revealing star sequences.", "usable": true, "use_location": "planetary_observation_deck", "use_object": "star_chart_console"}
    ],
    "puzzles": [
      {
        "puzzle_id": "stone_sequence_puzzle",
        "location": "observatory_main_chamber",
        "object": "stone_pedestal",
        "type": "sequence",
        "solution": ["stone1", "stone2", "stone3", "stone4"],
        "reward": "access_stonekeeper_sanctum",
        "description": "Arrange the carved stones on the pedestal in the correct sequence as hinted by the stone tablet."
      },
      {
        "puzzle_id": "star_chart_puzzle",
        "location": "planetary_observation_deck",
        "object": "star_chart_console",
        "type": "alignment",
        "solution": "correct_star_alignment",
        "reward": "activate_observatory_mechanism",
        "description": "Align the stars on the console according to the decoded text to activate the observatory mechanism."
      }
    ],
    "progression": [
      "Start at observatory_entrance.",
      "Talk to Kaelen at observatory_entrance.",
      "Move to observatory_main_chamber.",
      "Read stone_tablet in observatory_main_chamber.",
      "Talk to Anya in observatory_main_chamber.",
      "Move to stonekeeper_sanctum.",
      "Open stone_chest in stonekeeper_sanctum and obtain stone_sequence.",
      "Move back to observatory_main_chamber.",
      "Use stone_sequence on stone_pedestal in observatory_main_chamber to solve stone_sequence_puzzle and gain access to ancient_library.",      
      "Move to ancient_library.",
      "Read ancient_text in ancient_library and obtain decoded_text.",
      "Talk to Jax in ancient_library.",
      "Move to planetary_observation_deck.",
      "Use decoded_text on star_chart_console in planetary_observation_deck to solve star_chart_puzzle and activate observatory_mechanism.",      
      "Move to asteroid_field_transition.",
      "Move to distant_planet (Win)."
    ],
    "state_tracking": {
      "inventory": [],
      "puzzles_solved": [],
      "current_location": "observatory_entrance"
    },
    "win_condition": "Reach the distant_planet after activating the observatory mechanism.",
    "lose_condition": "Not explicitly defined in this logic (can be added later, e.g., time limit based on planetary cycles if needed).",
    "rules": [
      "Travel between areas is generally sequential as described in transitions.",
      "Stone Sequence is required to solve the Stone Pedestal puzzle.",
      "Decoded Text is required to solve the Star Chart Console puzzle.",
      "Solving puzzles unlocks new areas or progresses the story."
    ]
  }
}
```"""
            with progress_bar.container():
                st.progress(70)
            st.write("Loading game...")
            st.session_state.response = st.write_stream(start())
            if st.session_state.response:
                with progress_bar.container():
                    st.progress(100)
                st.rerun()

    options_container = st.container(border=True)
    
    col1, col2, col3 = options_container.columns([1,1,1])

    with options_container:
        with col1:
            st.download_button(data=save_game(), file_name="save_game.aitag", label="Save Game", use_container_width=True)
        with col2:
            st.button("Load Game", on_click=load_game, use_container_width=True)
        with col3:
            if st.button("End Game", use_container_width=True):
                keys = list(st.session_state.keys())
                for key in keys:
                    st.session_state.pop(key)
                st.session_state.second_run = True
                st.rerun()
        
                
            

    img_container = st.container(border=False)

    with img_container:
        img = st.empty()

    txt_container = st.container(height=200, border=True)

    input_container = st.container(border=False)

    with txt_container:
        txt = st.empty()

    if "first_run" in st.session_state and st.session_state.first_run == True:
        st.session_state.first_run = False

        img.image(get_placeholder_image())

        with txt_container:
            st.write(st.session_state.response)

        st.session_state.history.append(
            {
                "role": "model",
                "parts": [
                    st.session_state.response,
                ],
            }
        )
        description = image.describe_scene(st.session_state.response, st.session_state.history, st.session_state.logic)

        if description:
            new_image = fal.generate_image(description)
            if new_image:
                img.image(new_image)
                st.session_state.image = get_spinner(new_image)

    elif "story" not in st.session_state:
        st.write("Generating story...")
        st.session_state.story = text.generate_story()
        st.rerun()

    elif "logic" not in st.session_state:
        st.write("Generating logic...")
        st.session_state.logic = text.generate_game_logic(st.session_state.story)
        st.rerun()

    
    if prompt := st.chat_input("What would you do?"):
        
        img.image(st.session_state.image)
        
        st.session_state.history.append(
            {
                "role": "user",
                "parts": [
                    prompt,
                ],
            }
        )
        
        with txt_container:
            generator = text.generate_response(prompt, st.session_state.history, st.session_state.logic)
            response = st.write_stream(generator)
        if response:
            st.session_state.response = response
            
            description = image.describe_scene(st.session_state.response, st.session_state.history, st.session_state.logic)
            if description and not st.session_state.second_run:
                new_image = fal.generate_image(description)
                if new_image:
                    img.image(new_image)
                    st.session_state.image = get_spinner(new_image)
            if st.session_state.second_run:
                new_image = fal.generate_image("""Scene: Realistic, artistic, cinematic.
Setting: The entrance to an ancient observatory carved into a mountainside.
Visuals: Massive iron doors are set into the rock face, appearing old and weathered. The doors are sealed shut, with no visible handles or hinges. The overall lighting suggests natural daylight, casting shadows and highlighting the textures of the stone and metal.""")
                if new_image:
                    img.image(new_image)
                    st.session_state.image = get_spinner(new_image)

            st.session_state.history.append(
                {
                    "role": "model",
                    "parts": [
                        st.session_state.response,
                    ],
                }
            )
