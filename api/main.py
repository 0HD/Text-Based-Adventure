from fastapi import FastAPI
from engine import generate

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Server is working."}

@app.get("/generate/story")
async def get_story():
    return generate.generate_story()

@app.post("/generate/story")
async def post_story(keywords:str):
    return generate.generate_story(keywords)

@app.post("/generate/game_logic")
async def post_game_logic(story:str):
    pass