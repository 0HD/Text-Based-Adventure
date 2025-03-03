import fal_client, os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = os.path.abspath(os.path.join(BASEDIR, os.pardir))
BASEDIR = os.path.abspath(os.path.join(BASEDIR, os.pardir))

load_dotenv(os.path.join(BASEDIR, '.env'))

def generate_image(prompt):
    try:
        result = fal_client.subscribe(
            # replace with correct id from fal.ai
            "fal-ai/flux/schnell",
            arguments={
                "prompt": prompt,
                "image_size": "landscape_16_9",
                "num_inference_steps": 4,
                "num_images": 1,
                "enable_safety_checker": True,
                "seed": 0
            },
        )
    
        image = result["images"][0]["url"]
    
        from PIL import Image
        import requests
        from io import BytesIO
    
        response = requests.get(image)
        img = Image.open(BytesIO(response.content))
    
        return img
    except:
        return None
