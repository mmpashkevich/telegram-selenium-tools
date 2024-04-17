from pydantic import ValidationError

from datetime import datetime
import asyncio

from src.selenium_service.cache_manager import SeleniumCacheManager
from src.selenium_service.foreca import SeleniumForecaManager
from src.selenium_service.models import SeleniumApiForecaImage


class SeleniumService:
    def __init__(self):
        print('SeleniumService start init')

        self.cache_manager = SeleniumCacheManager()
        self.selenium_foreca = SeleniumForecaManager()
        print('SeleniumService initialized')

    def get_foreca_image(self) -> SeleniumApiForecaImage:
        try:
            image: SeleniumApiForecaImage = self._get_foreca_image_from_cache()
            if image and image.image_base64:
                return image
        except Exception as e:
            print(e)

    def _get_foreca_image_from_cache(self) -> SeleniumApiForecaImage:
        print('Get Foreca image from cache')
        try:
            image: SeleniumApiForecaImage = self.cache_manager.get_foreca_image()
            if image:
                return image
        except ValidationError as err:
            print(err.json())

    def _save_foreca_image_to_cache(self) -> SeleniumApiForecaImage:
        print('Saving Foreca image to cache')
        try:
            image_base64: bytes = self.selenium_foreca.get_image()
            if image_base64:
                image = SeleniumApiForecaImage(
                    name='weather_rostov_na_donu_' + datetime.now().strftime('%Y-%m-%dT%H:%M:%SUTC') + '.png',
                    image_base64=image_base64
                )
                self.cache_manager.save_foreca_image(image)
                return image
        except ValidationError as err:
            print(err.json())
        except Exception as e:
            print(e)

    async def loop_save_foreca_image_to_cache(self):
        print('Schedule save Foreca image to cache')
        while True:
            print('loop')
            self._save_foreca_image_to_cache()
            await asyncio.sleep(1)


if __name__ == "__main__":
    service = SeleniumService()
    asyncio.run(service.loop_save_foreca_image_to_cache())
