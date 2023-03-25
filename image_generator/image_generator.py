import json
import os
from base64 import b64decode
from pathlib import Path

import openai


class image_generator:
    """Image generator class using DALLE 2"""

    def __init__(self, api_key):
        self.api_key = api_key

    def generate_from_prompt(
        self, prompt, output_name=None, size="256x256", convert_to_png=True
    ):
        """Generate an image from a text prompt.

        Arguments:
            api_key (str): OpenAI API key.
            prompt (str): Text prompt for image generation.
            output_name (str): Name of output file.
            size (str): Size of output image.
            convert_to_png (bool): Convert output json to PNG.
        """
        if output_name is None:
            output_name = f"{prompt[:20]}.json"

        openai.api_key = self.api_key
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Number of images.
            size=size,  # 256x256, 512x512, or 1024x1024 pixels.
            response_format="b64_json",
        )
        response["prompt"] = prompt

        with open(output_name, mode="w", encoding="utf-8") as file:
            json.dump(response, file)

        print(f"File generated - {output_name}")

        if convert_to_png:
            self.convert_json_to_png(output_name)

    def generate_from_image(
        self, image_path, output_name=None, size="256x256", convert_to_png=True
    ):
        """Generate an image from another image.

        Arguments:
            api_key (str): OpenAI API key.
            image_path (str): Path to source image.
            output_name (str): Name of output file.
            size (str): Size of output image.
            convert_to_png (bool): Convert output json to PNG.
        """
        if output_name is None:
            output_name = f"{image_path.split('.')[0]}.json"

        openai.api_key = self.api_key
        response = openai.Image.create_variation(
            image=open(image_path, mode="rb"),
            n=1,  # Number of images.
            size=size,  # 256x256, 512x512, or 1024x1024 pixels.
            response_format="b64_json",
        )

        with open(output_name, mode="w", encoding="utf-8") as file:
            json.dump(response, file)

        print(f"File generated - {output_name}")

        if convert_to_png:
            self.convert_json_to_png(output_name)

    def convert_json_to_png(self, file_name):
        """Convert json to PNG.

        Arguments:
            file_name (str): Name of json file.
        """
        images = []

        with open(file_name, mode="r", encoding="utf-8") as file:
            response = json.load(file)

        for index, image_dict in enumerate(response["data"]):
            image_data = b64decode(image_dict["b64_json"])
            image_file = f"{file_name.split('.')[0]}-{index}.png"
            with open(image_file, mode="wb") as png:
                png.write(image_data)
            print(f"File converted - {image_file}")
            images.append(image_file)

        return images
