import random
from engine import client

wordlist = open("wordlist.txt", mode="r").read().splitlines()

def get_keywords(keywords = wordlist):
    return random.sample(keywords, 5)

def generate_story(keywords = get_keywords()):
    system_prompt = """You are a system prompt generator for a text-based AI game. Your task is to create a *detailed yet compact* system prompt describing a game world and story, based on 5 keywords. This prompt will guide a game logic generator.

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

    gemini = client.gemini.Model()
    
    gemini.set_system_prompt(system_prompt)

    import google.generativeai as genai
    gemini.set_structured_output(
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

    response = gemini.get_response("Generate a world based on these keywords: " + str(keywords), stream=False)

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
    
    

def generate_game_logic():
    pass

def generate_response(user_prompt, history, system_prompt):
    pass

def summarize_progression(history, system_prompt):
    pass

if __name__ == "__main__":
    pass