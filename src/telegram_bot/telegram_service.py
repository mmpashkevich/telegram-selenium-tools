from pydantic import ValidationError
from requests import Response
from src.selenium_service.models import SeleniumApiForecaImage, SeleniumApiImageResponse
import requests
import os


class TelegramService:
    def __init__(self):
        self.request_url = os.getenv('API_URL')

    def get_foreca_image(self) -> SeleniumApiForecaImage:
        try:
            response: Response = requests.get(self.request_url)
            data = response.json()
            if data.__contains__('success') and data['success']:
                image_response: SeleniumApiImageResponse = SeleniumApiImageResponse(**data)
                return image_response.image
        except ValidationError as err:
            print(err.json())


