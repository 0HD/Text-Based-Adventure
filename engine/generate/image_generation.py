from engine.client import gemini as ai

def describe_scene(prompt, history, logic):
    system_prompt = """You are a scene describer for scenes from a text-based adventure game, your output will be fed as an input into a diffusion model (FLUX schnell) to generate an image to be displayed to the user. Load the following JSON game logic to understand it as a reference only. You will not run the game logic. Below the JSON text, there will be a chat history of the interaction between the user prompts and the model representing the text-based game output. Also, the story will be revealed by the user interacting with a lot of things in the game, so don't include far-ahead spoilers in the scene description. The image (and your scene description in general) should not include things that violate Islamic culture or Saudi laws, and should not mention race, religion, creed, color, national origin, citizenship, marital status, sex, age, sexual orientation, gender identity, protected veteran status, political ideology, ancestry, the presence of any physical, sensory, or mental disabilities, or other legally protected status. The story might accidentally include some of those disallowed things, but the output should not mention/include them AT ALL COSTS, so be careful. They will not be moderated, it's your responsibility. You should not write anything unless you are 100% sure that it is allowed.
    DO NOT REPLY IN JSON. DESCRIBE A SCENE IN PLAIN TEXT NATURAL LANGUAGE.
    WHEN MENTIONING AN OBJECT NAME, DO NOT USE ITS JSON ID, USE ITS NAME THAT IS DEFINED IN THE JSON FILE, RIGHT UNDER THE ID. EXAMPLE: {"id": "grok", "name": "Beastkin Grok",...} USE "Beastkin Grok" INSTEAD OF "grok" WHEN GENERATING THE PROMPT.
    MAKE SURE THE SCENE DESCRIPTION MAKES IT CLEAR THAT THE IMAGE TO BE GENERATED SHOULD BE IN REALISTIC (BUT ARTISTIC) STYLE.
    FLUX PROMPTS ARE SIMILAR TO STABLE DIFFUSION PROMPTS. SO IF YOU'RE NOT FAMILIAR WITH FLUX PROMPTS, JUST PRETEND IT'S A STABLE DIFFUSION MODEL AND WRITE A PROMPT FOR IT.


    Here's the game logic as a reference ONLY:
    """


    system_prompt = system_prompt + logic
    
    system_prompt = system_prompt + """

    Here's the chat history as a reference ONLY:
    """

    system_prompt = system_prompt + str(history)

    system_prompt = system_prompt + """

    In the following user prompt here, you will be given the last response from the LLM model in the chat, as a scene to be described.
    Use it mainly, and the game logic earlier as a reference to understand what's going on, and the chat history to know what the user has seen before, to generate a scene description."""

    agent = ai.Model("gemini-2.0-flash-thinking-exp-01-21", history)
    agent.set_system_prompt(system_prompt)
    response = agent.get_response(prompt, stream=False)
    return response

if __name__ == "__main__":
    pass