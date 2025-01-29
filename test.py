from engine.generate import text_generation as text
from engine.client import fal

story = text.generate_story()

print(story)
print("=========================")

logic = text.generate_game_logic(story)

print(logic)
print("=========================")

history = [
    {
      "role": "user",
      "parts": [
        "Hello",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The user says \"Hello\". This is the start of the game.\nI should greet the user and present the starting location, which is Crossroads according to the game data and progression path.\nI should also list the available objects and interactions at the Crossroads.",
        "You are at Crossroads.\nDescription: A central junction where paths diverge towards the Forest, Citadel, and City. A wrecked car lies nearby.\nObjects: Signpost, Wrecked Car, Traveler.\n\nWhat do you want to do? (examine signpost, examine car, talk to traveler)",
      ],
    },
    {
      "role": "user",
      "parts": [
        "examine car",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The user chose to \"examine car\". I need to describe the wrecked car in detail from the JSON and list available interactions.",
        "You examine the Wrecked Car.\nDescription: A magically powered car, heavily damaged and smoking. Arcane energy crackles around it.\nInteractions: (take arcane shard)\n\nWhat do you want to do? (take arcane shard)",
      ],
    },
    {
      "role": "user",
      "parts": [
        "take arcane shard",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The user wants to take the arcane shard.\nI need to check if this is a valid interaction for the 'Wrecked Car' object.\nYes, \"take arcane shard\" is listed as an interaction.\nI need to update the inventory of the player to include the arcane shard.\nI also need to provide feedback to the user that they have taken the arcane shard and describe the item.\nAfter taking the shard, what are the available actions at the Crossroads location?  The available objects are Signpost, Wrecked Car, and Traveler.  The available interactions are examine signpost, talk to traveler.  For the wrecked car, there are no more listed interactions after taking the shard.",
        "You take the Arcane Shard.\nInventory updated: Arcane Shard added.\nArcane Shard: A fragment of magically charged crystal, found at the car crash. Emits a faint energy.\n\nYou are at Crossroads.\nDescription: A central junction where paths diverge towards the Forest, Citadel, and City. A wrecked car lies nearby.\nObjects: Signpost, Wrecked Car, Traveler.\n\nWhat do you want to do? (examine signpost, talk to traveler)",
      ],
    },
    {
      "role": "user",
      "parts": [
        "what do i have",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The user is asking to check their inventory. I need to access the `state_tracking.inventory` from the JSON and display its contents.",
        "Inventory: Arcane Shard.\n\nYou are at Crossroads.\nDescription: A central junction where paths diverge towards the Forest, Citadel, and City. A wrecked car lies nearby.\nObjects: Signpost, Wrecked Car, Traveler.\n\nWhat do you want to do? (examine signpost, talk to traveler)",
      ],
    },
    {
      "role": "user",
      "parts": [
        "what does it do",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The user is asking about the Arcane Shard in their inventory. I need to retrieve the description of the Arcane Shard from the game data and display it to the user. Then, I need to remind the user of their current location and available actions.",
        "Arcane Shard: A fragment of magically charged crystal, found at the car crash. Emits a faint energy.\n\nYou are at Crossroads.\nDescription: A central junction where paths diverge towards the Forest, Citadel, and City. A wrecked car lies nearby.\nObjects: Signpost, Wrecked Car, Traveler.\n\nWhat do you want to do? (examine signpost, talk to traveler)",
      ],
    },
    {
      "role": "user",
      "parts": [
        "talk to traveler",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The user wants to talk to the traveler. I need to check if there is a traveler NPC defined in the 'crossroads' area in the JSON. I see \"Traveler\" object with \"npc_id\": \"traveler_npc\".  However, I need to check the \"npcs\" list to see if there is an NPC with id \"traveler_npc\".  Looking at the \"npcs\" list, there are NPCs with ids 'kaelan', 'zara', 'eldrin', and 'pyralia', but no 'traveler_npc'.\n\nThis means the \"Traveler\" object in \"crossroads\" is just a flavor object and not linked to an actual NPC with dialogue in the JSON.\n\nTherefore, talking to the traveler will not yield any dialogue from a defined NPC. I should respond in a way that reflects this, perhaps a generic traveler dialogue or indicate that the traveler is not talkative.  Since the JSON doesn't provide dialogue for a traveler NPC, I will assume they are not talkative.\n\nLet's provide a response like: \"You attempt to talk to the Traveler, but they seem weary and uninterested in conversation.\"  Then, offer the available actions again.",
        "You talk to the Traveler.\nThe traveler is weary and does not seem interested in talking.\n\nYou are at Crossroads.\nDescription: A central junction where paths diverge towards the Forest, Citadel, and City. A wrecked car lies nearby.\nObjects: Signpost, Wrecked Car, Traveler.\n\nWhat do you want to do? (examine signpost)",
      ],
    },
    {
      "role": "user",
      "parts": [
        "say hi",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The user wants to \"say hi\" to the traveler. However, \"talk to traveler\" has already been attempted and the traveler is weary and not interested in talking.  \"say hi\" is essentially the same intent as \"talk to traveler\".  The game logic doesn't have a specific \"say hi\" interaction for the traveler, only \"talk to traveler\" which has already resulted in a negative response.  Therefore, repeating a similar action is unlikely to yield a different result.  I should respond based on the previous interaction, indicating the traveler is still uninterested.\n\n**Response Strategy:**\n\n1. **Recall previous interaction:** Remember the traveler is weary and not talkative.\n2. **Interpret \"say hi\" as attempt to interact:**  Recognize it's another attempt to engage the traveler.\n3. **Reiterate traveler's state:**  Reinforce that the traveler is still weary and uninterested.\n4. **Offer other options:**  Guide the user back to available actions at the Crossroads.",
        "You attempt to greet the Traveler, but they wave a hand dismissively, eyes closed, clearly wanting to rest undisturbed.  They don't respond to your greeting.\n\nYou are at Crossroads.\nDescription: A central junction where paths diverge towards the Forest, Citadel, and City. A wrecked car lies nearby.\nObjects: Signpost, Wrecked Car, Traveler.\n\nWhat do you want to do? (examine signpost)",
      ],
    },
    {
      "role": "user",
      "parts": [
        "where am i",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The user is asking about their current location in the game. I need to provide the current location name and description.  The current location is Crossroads. I should also remind the user of the available actions at this location.",
        "You are at Crossroads.\nDescription: A central junction where paths diverge towards the Forest, Citadel, and City. A wrecked car lies nearby.\nObjects: Signpost, Wrecked Car, Traveler.\n\nWhat do you want to do? (examine signpost)",
      ],
    },
    {
      "role": "user",
      "parts": [
        "ask him where am i",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The user wants to ask the traveler \"where am I?\".  However, the traveler is described as weary and uninterested in talking.  The game has already shown the traveler is dismissive and doesn't want to be disturbed.  Therefore, even if the user *asks* the traveler, the traveler will likely not respond or give a dismissive answer.  I should reflect the traveler's disinterest.  Let's assume the traveler grunts a dismissive answer rather than being helpful.",
        "You ask the Traveler \"Where am I?\".\n\nThe Traveler sighs, barely opening their eyes. \"Crossroads,\" they mumble, \"Now leave me be.\"\n\nYou are at Crossroads.\nDescription: A central junction where paths diverge towards the Forest, Citadel, and City. A wrecked car lies nearby.\nObjects: Signpost, Wrecked Car, Traveler.\n\nWhat do you want to do? (examine signpost)",
      ],
    },
    {
      "role": "user",
      "parts": [
        "update the game so that it matches the new game logic in the system prompt",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The user wants me to read the system prompt again and use the new game logic and story from the JSON, and obey the constraints in the system prompt. I should reply to the user in natural language only from now on. I'm not sure if the user wants to play immediately, so I will ask them to say a word like 'Start' to start the new game."
        "Alright, say 'Start' to start the new game.",
      ],
    },
]

from rich.console import Console

console = Console()

from engine.generate import image_generation as image

while True:
  console.print("\nYour input: ", end='', style='bold cyan')
  user_prompt = input()
  history.append(
    {
      "role": "user",
      "parts": [
        user_prompt,
      ],
    }
  )
  model_response = ""
  print()
  response = text.generate_response(user_prompt, history, logic)
  console.print(response, end='', style='italic yellow')
  history.append(
    {
      "role": "model",
      "parts": [
        response,
      ],
    }
  )

  print(fal.generate_image(image.describe_scene(response, history, logic)))

