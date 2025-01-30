import random
from engine.client import gemini as ai

wordlist = open("wordlist.txt", mode="r").read().splitlines()

def get_guide_history():
    return [
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

def get_keywords(keywords = wordlist):
    return random.sample(keywords, 5)

def generate_story(keywords = get_keywords()):
    system_prompt = """You are a system prompt generator for a text-based AI game. Your task is to create a *detailed yet compact* system prompt describing a game world and story, based on 5 keywords. This prompt will guide a game logic generator. The story (and thus game) should not include things that violate Islamic culture or Saudi laws, and should not mention race, religion, creed, color, national origin, citizenship, marital status, sex, age, sexual orientation, gender identity, protected veteran status, political ideology, ancestry, the presence of any physical, sensory, or mental disabilities, or other legally protected status. The keywords might accidentally imply some of those disallowed things, but the story should not mention/include them AT ALL COSTS, so be careful. They will not be moderated, it's your responsibility. You should not write anything unless you are 100% sure that it is allowed. No crosses, no temples, no worshipping, and nothing that violates what I said earlier.

**Instructions:**

1.  **Keyword Integration & Expansion:** Integrate all 5 keywords meaningfully. List keywords at the start.  Then, *expand* on each keyword within the descriptions to create richer, more evocative details.

2.  **Detailed Compact System Prompt Output:** Your *entire output* is a ready-to-use system prompt.  Maintain a compact, machine-friendly style, but provide *significantly more detail* within each bullet point using descriptive keywords and short phrases.

3.  **System Prompt Structure (Detailed Compact):**

    ```
    You are a text-based adventure game world.

    World:
    * Setting: [Descriptive setting -  locations, atmosphere, using keywords to create vivid but brief picture]
    * Rules: [Key world rules -  how things work, limitations, using keywords to define mechanics and logic]
    * Factions: [Factions/Groups -  describe factions, their goals, and relationships, using keywords to define them concisely]
    * NPCs: [Important NPCs - Names, roles, motivations, very brief personality hints, using keywords to make them memorable]
    * Plot Hooks: [Intriguing Starting Scenarios -  brief descriptions of initial conflicts or mysteries, using keywords to set the stage]
    * Story: [Overarching Story -  a concise but evocative summary of the central conflict and themes, using keywords to define the narrative]
    * Objective: [Player Objective -  a clear, engaging goal for the player within this world, using keywords to make it impactful]
    ```

4.  **Descriptive Keywords and Phrases:**  Within each bullet point, use *descriptive keywords and short phrases* to build a more detailed picture.  Think "compressed detail" – pack as much information as possible into concise, evocative language.

5.  **Focus on Richness within Compactness:**  Aim for a balance.  Be concise overall in structure and sentence length, but be *rich in descriptive detail* within each bullet point.  The goal is to provide a more substantial foundation for the game logic generator.

**Do not include extra explanations. Generate only the detailed compact system prompt based on keywords.**"""

    agent = ai.Model()
    
    agent.set_system_prompt(system_prompt)

    import google.generativeai as genai
    agent.set_structured_output(
        genai.protos.Schema(
            type = genai.protos.Type.OBJECT,
            enum = [],
            required = ["keywords", "system_prompt", "world_details"],
            properties = {
            "keywords": genai.protos.Schema(
                type = genai.protos.Type.ARRAY,
                description = "List of 5 keywords",
                items = genai.protos.Schema(
                type = genai.protos.Type.STRING,
                ),
            ),
            "system_prompt": genai.protos.Schema(
                type = genai.protos.Type.STRING,
                description = "Detailed compact system prompt for text-based adventure game world",
            ),
            "world_details": genai.protos.Schema(
                type = genai.protos.Type.OBJECT,
                enum = [],
                required = ["setting", "rules", "factions", "npcs", "plot_hooks", "story", "objective"],
                properties = {
                "setting": genai.protos.Schema(
                    type = genai.protos.Type.STRING,
                    description = "Descriptive setting - locations, atmosphere, using keywords to create vivid but brief picture",
                ),
                "rules": genai.protos.Schema(
                    type = genai.protos.Type.STRING,
                    description = "Key world rules - how things work, limitations, using keywords to define mechanics and logic",
                ),
                "factions": genai.protos.Schema(
                    type = genai.protos.Type.STRING,
                    description = "Factions/Groups - describe factions, their goals, and relationships, using keywords to define them concisely",
                ),
                "npcs": genai.protos.Schema(
                    type = genai.protos.Type.STRING,
                    description = "Important NPCs - Names, roles, motivations, very brief personality hints, using keywords to make them memorable",
                ),
                "plot_hooks": genai.protos.Schema(
                    type = genai.protos.Type.STRING,
                    description = "Intriguing Starting Scenarios - brief descriptions of initial conflicts or mysteries, using keywords to set the stage",
                ),
                "story": genai.protos.Schema(
                    type = genai.protos.Type.STRING,
                    description = "Overarching Story - a concise but evocative summary of the central conflict and themes, using keywords to define the narrative",
                ),
                "objective": genai.protos.Schema(
                    type = genai.protos.Type.STRING,
                    description = "Player Objective - a clear, engaging goal for the player within this world, using keywords to make it impactful",
                ),
                },
            ),
            },
        )
    )

    response = agent.get_response("Generate a world based on these keywords: " + str(keywords), stream=False)

    import json
    j = json.loads(response)

    return f"""\
World description:
Setting: {j['world_details']['setting']}
Rules: {j['world_details']['rules']}
Factions: {j['world_details']['factions']}
NPCs: {j['world_details']['npcs']}
Plot Hooks: {j['world_details']['plot_hooks']}
Story: {j['world_details']['story']}
Objective: {j['world_details']['objective']}\
"""
    # end of function
    
    

def generate_game_logic(story:str):
    system_prompt = """You are a system prompt generator specializing in designing text-based adventure game logic. Your task is to generate the core game logic based on a provided world description and story. This logic will be used as a system prompt for another AI that will play the game with a user. The story (and thus logic) should not include things that violate Islamic culture or Saudi laws, and should not mention race, religion, creed, color, national origin, citizenship, marital status, sex, age, sexual orientation, gender identity, protected veteran status, political ideology, ancestry, the presence of any physical, sensory, or mental disabilities, or other legally protected status. The story might accidentally include some of those disallowed things, but the logic should not mention/include them AT ALL COSTS, so be careful. They will not be moderated, it's your responsibility. You should not write anything unless you are 100% sure that it is allowed. No crosses, no temples, no worshipping, and nothing that violates what I said earlier.

**Input:**

You will be given a detailed world description and story. This information contains rules, settings, and narrative elements that define the game world.

**Task:**

Based on the provided world and story, generate a structured game logic. This logic should include, but is not limited to:

*   **Levels/Areas:** Define distinct locations or areas the player will navigate. Consider the relationships between these areas (e.g., adjacency, access requirements). Describe each area briefly to keep it machine-readable.
*   **Objects:** Identify interactive objects within each area. This includes items, containers (chests, boxes), doors, obstacles, and puzzle elements. Specify their properties, interactions, and unique IDs.
*   **NPCs (Non-Player Characters):** Define any characters the player will encounter. Include their names, locations, roles, basic dialogue, and any relevant information they might possess.
*   **Items:** List all obtainable items, including their properties (e.g., is it usable, what does it do, is it a key, a weapon, consumable) and locations where they can be found.
*   **Puzzles:** Design any puzzles, including their mechanics, solutions, and any rewards for solving them.
*   **Progression:** Outline a logical progression path for the player. This should include how the player moves between areas, unlocks new content, and achieves goals.
*   **State Tracking:** Identify key game states that need to be tracked (e.g., player inventory, completed puzzles, NPC relationships). Provide a way to represent these states.
*   **Win/Lose Conditions:** Define clear criteria for winning or losing the game.
*   **Rules:** Enforce the world's rules and settings, including limitations on player actions or interactions.

Your output will be used as a system prompt for a new instance of Gemini. Do not reply to the user. There is no user."""
    
    agent = ai.Model("gemini-2.0-flash-thinking-exp-01-21")
    agent.set_temperature(0.3)
    agent.set_system_prompt(system_prompt)
    
    response = agent.get_response(story, stream=False)

    return response


def generate_response(user_prompt, history, logic):
    system_prompt = """You are a text-based game. Load the following JSON as game logic, and play with the user. Your output should be clear and concise, just like a text-based game. You are not a storyteller. The story will be revealed by interacting with a lot of things in the game. The game (and your output in general) should not include things that violate Islamic culture or Saudi laws, and should not mention race, religion, creed, color, national origin, citizenship, marital status, sex, age, sexual orientation, gender identity, protected veteran status, political ideology, ancestry, the presence of any physical, sensory, or mental disabilities, or other legally protected status. The story might accidentally include some of those disallowed things, but the output should not mention/include them AT ALL COSTS, so be careful. They will not be moderated, it's your responsibility. You should not write anything unless you are 100% sure that it is allowed. No crosses, no temples, no worshipping, and nothing that violates what I said earlier.
    DO NOT REPLY IN JSON. REPLY TO THE USER IN PLAIN TEXT NATURAL LANGUAGE. THE USER IS PLAYING WITH YOU THE GAME. DO NOT REPEAT ANYTHING FROM THIS SYSTEM PROMPT TO THE USER. DO NOT EXPLAIN THE STORY. IT WILL NATURALLY BE REVEALED THROUGH A LOT OF INTERACTIONS THROUGHOUT THE GAME.
    WHEN MENTIONING AN OBJECT, DO NOT USE ITS JSON ID, USE ITS NAME THAT IS DEFINED IN THE JSON FILE, RIGHT UNDER THE ID. EXAMPLE: {"id": "grok", "name": "Beastkin Grok",...} USE "Beastkin Grok" INSTEAD OF "grok" WHEN GENERATING THE PROMPT.
    HAVE SOME CREATIVITY WHEN GOING OFF-SCRIPT, SUCH AS THE USER INTERACTING WITH NPCs IN UNEXPECTED WAYS, AND PLAY ALONG, AND MAKE IT AFFECT THE GAME CONSEQUENCES LATER ON.
    USE MARKDOWN EXTENSIVELY. WHEN IT COMES TO STORY-TELLING OR SCENE-TELLING, BE SUPER CONCISE. FOR EXAMPLE, WHEN DESCRIBING A VERY DRAMATIC SCENE, MAKE IT AS SHORT AS POSSIBLE, WHILE KEEPING ALL THE DETAILS.
    Here's the game logic to start the game:
    """

    system_prompt = system_prompt + logic

    agent = ai.Model("gemini-2.0-flash-thinking-exp-01-21", history)
    agent.set_system_prompt(system_prompt)
    response = agent.get_response(user_prompt, stream=True)
    return response

if __name__ == "__main__":
    pass