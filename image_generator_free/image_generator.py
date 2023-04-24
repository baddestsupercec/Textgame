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
        size=512,
        restore_faces=True,
        num_images=1,
        steps=10,
        cfg_scale=7,
    ):
        """Generate an image from a text prompt.

        See https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/txt2img.py for api args

        Arguments:
            data (str): input data.
            input_type (str): Type of input. Must be either "prompt" or "image".
            output_name (str): Name of output file.
            size (str): Size of generated image. sizexsize.
            restore_faces (bool): Whether to restore faces in generated images.
            num_images (int): Number of images to generate.
            steps (int): Number of steps to run the model for.
            cfg_scale (int): Classifier free guidance scale. How strongly the image should conform to the prompt.
        """
        # Set output_name if none provided.
        if output_name is None:
            output_name = data[:20]

        full_path = f"{self.img_write_dir}{output_name}.png"

        if input_type == "prompt":
            send_data = {  # Specify the config for the generated images.
                "sd_model": "v2-1_768-ema-pruned.safetensors",
                "prompt": data,
                "negative_prompt": "text, lowres, error, cropped, worst quality, low quality, jpeg artifacts, out of frame, watermark, signature",
                "width": size,
                "height": size,
                "restore_faces": restore_faces,
                "tiling": False,
                "batch_size": num_images,
                "steps": steps,
                "cfg_scale": cfg_scale,
            }
            response = self._submit_post(self.api_url, send_data)
            self._save_encoded_image(response.json()["images"][0], full_path)
        elif input_type == "image":
            raise NotImplementedError("Image input not yet implemented.")
        else:
            raise ValueError("Argument 'input_type' must one of 'prompt', 'image'.")
