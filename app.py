
import streamlit as st
from engine.generate import text_generation as text
from engine.generate import image_generation as image
from engine.client import fal

if "story" not in st.session_state and "logic" not in st.session_state:
    st.write("Generating story...")
    st.session_state.story = text.generate_story()
    st.write(st.session_state.story)
    st.write("Generating logic...")
    st.session_state.logic = text.generate_game_logic(st.session_state.story)
    st.write(st.session_state.logic)
    st.rerun()

elif "story" not in st.session_state:
    st.write("Generating story...")
    st.session_state.story = text.generate_story()
    st.rerun()

elif "logic" not in st.session_state:
    st.write("Generating logic...")
    st.session_state.logic = text.generate_game_logic(st.session_state.story)
    st.rerun()

if "history" not in st.session_state:
    st.session_state.history = text.get_guide_history()

st.title("AI-Powered Text-Based Adventure")

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

img = st.empty()

if "image" not in st.session_state:
    st.session_state.image = get_placeholder_image()

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
    
    with st.chat_message("assistant"):
        generator = text.generate_response(prompt, st.session_state.history, st.session_state.logic)
        response = st.write_stream(generator)
    if response:
        st.session_state.response = response
        
        description = image.describe_scene(st.session_state.response, st.session_state.history, st.session_state.logic)
        if description:
            new_image = fal.generate_image(description)
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
