import os

from dotenv import load_dotenv

from image_generator import image_generator as ig

# Requires .env file with OpenAI API key.
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Instantiate class with API key.
ig1 = ig(openai_key)
# Create image using prompt.
prompt_1 = "A cure in a hospital in a zombie apocalypse"
images = ig1.generate_from_prompt(prompt_1)
print(images)

# Convert json file to png.
json_1 = "An abandoned hospital in a zombie apocalypse.json"
ig1.convert_json_to_png(json_1)

# Create image from image
ig2 = ig(openai_key)
image_path = "test.png"
ig2.generate_from_image(image_path)
