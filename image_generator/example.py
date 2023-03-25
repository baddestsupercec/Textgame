import os

from dotenv import load_dotenv

from image_generator import image_generator as ig

# Requires .env file with OpenAI API key.
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Create image using prompt.
ig1 = ig(openai_key)
prompt_1 = "A cure in a hospital in a zombie apocalypse"
images = ig1.generate(prompt_1, input_type="prompt")
print(images)

# Convert json file to png.
json_1 = "An abandoned hospital in a zombie apocalypse.json"
ig1._convert_json_to_png(json_1)

# Create image from image
ig2 = ig(openai_key)
image_path = "test.png"
images_2 = ig2.generate(image_path, input_type="image")
print(images_2)
