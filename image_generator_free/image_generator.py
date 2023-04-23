import json
import os
import base64
import requests

from base64 import b64decode
from pathlib import Path


class image_generator:
    """Image generator class using DALLE 2"""

    def __init__(self, img_write_dir, api_url):
        """
        Arguments:
            img_write_dir (str): Directory to write images to.
            api_url (str): URL of API.
        """
        self.img_write_dir = img_write_dir
        self.api_url = api_url

    def _submit_post(self, url: str, data: dict):
        """
        Submit a POST request to the given URL with the given data.
        """
        return requests.post(url, data=json.dumps(data))

    def _save_encoded_image(self, b64_image: str, output_path: str):
        """
        Save the given image to the given output path.
        """
        with open(output_path, "wb") as image_file:
            image_file.write(base64.b64decode(b64_image))

    def generate(
        self,
        data,
        input_type,
        output_name=None,
        num_images=1,
        size=256,
    ):
        """Generate an image from a text prompt.

        Arguments:
            data (str): input data.
            input_type (str): Type of input. Must be either "prompt" or "image".
            output_name (str): Name of output file.
            num_images (int): Number of images to generate.
            size (str): Size of output image. 256x256, 512x512, or 1024x1024 pixels.
        """
        # Set output_name if none provided.
        if output_name is None:
            output_name = data[:20]

        full_path = f"{self.img_write_dir}{output_name}.png"

        if input_type == "prompt":
            send_data = {"prompt": data, "width": size, "height": size}
            response = self._submit_post(self.api_url, send_data)
            self._save_encoded_image(response.json()["images"][0], full_path)
        elif input_type == "image":
            raise NotImplementedError("Image input not yet implemented.")
        else:
            raise ValueError("Argument 'input_type' must one of 'prompt', 'image'.")