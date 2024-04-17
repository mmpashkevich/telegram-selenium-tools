import os
import json

from src.selenium_service.models import SeleniumApiForecaImage


class SeleniumCacheManager:
    def __init__(self):
        self.path_cache_dir = os.getcwd() + '/.cache/'
        self.path_image_file = self.path_cache_dir + 'weather_rostov_na_donu.json'

        if not os.path.exists(self.path_cache_dir):
            os.makedirs(self.path_cache_dir)

    def get_foreca_image(self) -> SeleniumApiForecaImage:
        print('get from cache')
        if os.path.exists(self.path_image_file):
            with open(self.path_image_file, 'r') as f:
                d: dict = json.load(f)
                if len(d) > 0:
                    image: SeleniumApiForecaImage = SeleniumApiForecaImage(**d)
                    return image
        else:
            raise NotADirectoryError

    def save_foreca_image(self, image_object: SeleniumApiForecaImage):
        print('saving to cache')
        with open(self.path_image_file, 'w+') as f:
            f.write(image_object.model_dump_json())
        if os.path.exists(self.path_image_file):
            print('saved Foreca image to cache', self.path_image_file)
        else:
            raise FileExistsError