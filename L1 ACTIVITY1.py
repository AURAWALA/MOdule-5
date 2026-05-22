from huggingface_hub import InferenceClient
from datetime import datetime
from PIL import Image
from config import HF_API_KEY

MODELS = [
    "ByteDance/SDXL-Lighting",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/sdxl-turbo",
    "runwayml/stable-diffusion-v1-5",
]

client = InferenceClient(api_key=HF_API_KEY)

print(f"Primary model: {MODELS[0]}")
print("Type 'quit' to exit\n")

while True:
    prompt = input("Enter your prompt: ").strip()
    if prompt.lower() in ["quit", "exit", "q"]:
        break
    if not prompt:
        continue

    print("Generating image...")
    
    for model in MODELS:
        try:
            image = client.text_to_image(prompt, model=model)
            break
        except Exception:
            print(f"  Executing next....   ")
            continue

    if image:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")   
        filename = f"generated_{timestamp}.png"
        image.save(filename)
        print(f"Image saved as {filename}")
        image.show()
        print()
    else:
        print("Error: All models failed to generate an image.Check your api key.\n")     

print("Goodbye!")        
