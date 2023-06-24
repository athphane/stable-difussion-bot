import base64
import io
import os

import requests
from PIL import Image, PngImagePlugin

from stablebot.stable_difussion.utils import generate_filename


class StableDiffusion:
    def __init__(self):
        self.url = os.environ['SD_URL']

    def __generate_url(self, path: str):
        path = path.lstrip('/')

        return f'{self.url}/{path}'

    def _get(self, path):
        response = requests.get(url=self.__generate_url(path))
        return response.json()

    def _post(self, path: str, json: object):
        response = requests.post(url=self.__generate_url(path), json=json)
        return response.json()

    def generate_image(self, prompt: str, steps: int = 10):
        payload = {
            "prompt": prompt,
            "steps": steps,
            "negative_prompt": "lowres, (bad anatomy:1.2), close shot,(textured skin:1.3),(no background:1.2),"
                               "multiple views, deformed, six fingers, child, black & white, monochrome, "
                               "(bad hands:1.2), (text:1.2), error, cropped, worst quality, low quality, "
                               "normal quality, jpeg artifacts, (signature:1.2), (watermark:1.3), username, blurry, "
                               "out of focus, censorship, old, amateur drawing, colored, stylized, shading, "
                               "displaced feet, out of frame "
        }

        response = self._post('/sdapi/v1/txt2img', payload)

        generated_files = []

        for i in response['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

            png_payload = {
                "image": "data:image/png;base64," + i
            }

            response2 = self._post('/sdapi/v1/png-info', png_payload)

            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2['info'])

            file_name = generate_filename()
            image.save(file_name, pnginfo=pnginfo)
            generated_files.append(file_name)

        return generated_files

    def get_models(self):
        return self._get('/sdapi/v1/sd-models')

    def change_model(self, selected_model):
        response = self._post('/sdapi/v1/options', {'sd_model_checkpoint': selected_model})
        return True if response is None else False
