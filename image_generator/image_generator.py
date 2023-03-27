import json
import os
from base64 import b64decode
from pathlib import Path

import openai


class image_generator:
    """Image generator class using DALLE 2"""

    def __init__(self, api_key):
        """
        Arguments:
            api_key (str): OpenAI API key.
        """
        self.api_key = api_key

    def generate(
        self,
        data,
        input_type,
        output_name=None,
        num_images=1,
        size="256x256",
        convert_to_png=True,
    ):
        """Generate an image from a text prompt.

        Arguments:
            data (str): input data.
            input_type (str): Type of input. Must be either "prompt" or "image".
            output_name (str): Name of output file.
            num_images (int): Number of images to generate.
            size (str): Size of output image. 256x256, 512x512, or 1024x1024 pixels.
            convert_to_png (bool): Convert output json to PNG.
        """
        # Set output_name if none provided.
        if output_name is None:
            output_name = data[:20]

        # Set API Key.
        openai.api_key = self.api_key

        if input_type == "prompt":
            response = openai.Image.create(
                prompt=data,
                n=num_images,
                size=size,
                response_format="b64_json",
            )
            response["prompt"] = data
        elif input_type == "image":
            response = openai.Image.create_variation(
                image=open(image_path, mode="rb"),
                n=num_images,
                size=size,
                response_format="b64_json",
            )
        else:
            raise ValueError("Argument 'input_type' must one of 'prompt', 'image'.")

        # Append creation time to make unique filename & '.json'
        output_name = output_name + f"-{response['created']}" + ".json"

        with open(output_name, mode="w", encoding="utf-8") as file:
            json.dump(response, file)

        print(f"File generated - {output_name}")

        if convert_to_png:
            return self._convert_json_to_png(output_name)

    def _convert_json_to_png(self, file_name):
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
