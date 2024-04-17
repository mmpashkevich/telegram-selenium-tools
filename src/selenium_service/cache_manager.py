import os
import json

from src.selenium_service.models import SeleniumApiForecaImage


class SeleniumCacheManager:
    def __init__(self):
        self.path_cache_dir = os.getcwd() + '/.cache/'
        self.path_cache_foreca_image_json = self.path_cache_dir + 'foreca-rostov-na-donu-image.json'

        if not os.path.exists(self.path_cache_dir):
            os.makedirs(self.path_cache_dir)

    def get_foreca_image(self) -> SeleniumApiForecaImage:
        with (open(self.path_cache_foreca_image_json, 'r') as f):
            d: dict = json.load(f)
            if len(d) > 0:
                image: SeleniumApiForecaImage = SeleniumApiForecaImage(**d)
                return image

    def save_foreca_image(self, data: SeleniumApiForecaImage):
        open(self.path_cache_foreca_image_json, 'w+').write(data.model_dump_json())

if __name__ == '__main__':
    d = dict(name='test', image_base64=None)

    image: SeleniumApiForecaImage = SeleniumApiForecaImage(**d)