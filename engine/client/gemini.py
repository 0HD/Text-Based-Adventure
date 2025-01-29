import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = os.path.abspath(os.path.join(BASEDIR, os.pardir))
BASEDIR = os.path.abspath(os.path.join(BASEDIR, os.pardir))

load_dotenv(os.path.join(BASEDIR, '.env'))

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_KEY"))

def create_model(
        model = "gemini-2.0-flash-exp",
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 65536,
            "response_mime_type": "text/plain"
        },
        system_prompt = "You are a helpful assistant."
):
    model = genai.GenerativeModel(
        model_name = model,
        generation_config = generation_config,
        system_instruction = system_prompt,
    )

    return model

def create_chat(model = create_model(), new_history = []):
    return model.start_chat(history=new_history)

def send_message(prompt:str, chat_session = create_chat(), stream = True):
    return chat_session.send_message(prompt, stream=stream)

class Model():
    def __init__(self, model_name = None, history = []):
        self.config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 65536,
            "response_mime_type": "text/plain"
        }
        if model_name == None:
            self.model_name = "gemini-2.0-flash-exp"
        else:
            self.model_name = model_name
        self.system_prompt = "You are a helpful assistant."
        self.model = create_model(self.model_name, self.config, self.system_prompt)
        self.chat = create_chat(self.model, history)

    def get_streamed_response(self, prompt:str):
        response = send_message(prompt, self.chat, stream=True)
        from random import randint
        from time import sleep

        for chunk in response:
            counter = 0
            t = 16
            while True:
                r = randint(2, 10)
                split = chunk.text[counter : counter + r]
                sleep(t/1000)
                yield split
                if counter >= len(chunk.text):
                    break
                counter = counter + r
                try:
                    x = response.text
                except:
                    t = 16
                else:
                    t = 10

    def get_response(self, prompt:str, stream:bool = True):
        if stream:
            return self.get_streamed_response(prompt)
        else:
            # response = send_message(prompt, self.chat, stream=False)
            response = self.chat.send_message(prompt, stream = False)
            return response.text
    
    def update_model(self):
        self.model = create_model(self.model_name, self.config, self.system_prompt)
        self.chat = create_chat(self.model, self.chat.history)

    def set_temperature(self, temperature:float):
        self.config["temperature"] = temperature
        self.update_model()

    def set_max_output_tokens(self, max:int):
        self.config["max_output_tokens"] = max
        self.update_model()
    
    def set_system_prompt(self, prompt:str):
        self.system_prompt = prompt
        self.update_model()
    
    def set_model_name(self, name:str):
        self.model_name = name
        self.update_model()
    
    def set_history(self, history):
        self.chat = create_chat(self.model, history)
    
    def clear_history(self):
        self.set_history([])
    
    def set_structured_output(self, structure):
        self.config["response_schema"] = structure
        self.config["response_mime_type"] = "application/json"
        self.update_model()
    
    def drop_structured_output(self):
        self.config.pop("response_schema", None)
        self.config["response_mime_type"] = "text/plain"
        self.update_model()

        



if __name__ == "__main__":
    pass