from requests.models import Response
import requests
from src.telegram_bot.telegram_service import TelegramService
from src.selenium_service.models import SeleniumApiForecaImage


class MockResponse(Response):
    def __init__(self, json_mock):
        self.json_mock = json_mock
        super(MockResponse, self).__init__()

    def json(self):
        return self.json_mock

class MockReponse:
    mock_success_telegram_response = dict(success=True, image=dict(name='mock_name', url='mock_url',
                                                                   image_base64=b'mock base64 string'))
    mock_error_telegram_response = dict(success=False, error='Ouch! ERROR!')
    mock_image_object_telegram_response = dict(success=True,
                                                        image=dict(name='mock_name', invalid_image_object=True))
    mock_invalid_telegram_response = dict(success=True, image=None)

class TestTelegramService:
    def test_success_get_foreca_image(self, mocker):
        mocker.patch.object(requests, 'get', return_value=MockResponse(MockReponse.mock_success_telegram_response))
        service = TelegramService()
        result = service.get_foreca_image()
        assert isinstance(result, SeleniumApiForecaImage)


    def test_error_response_get_foreca_image(self, mocker):
        mocker.patch.object(requests, 'get', return_value=MockResponse(MockReponse.mock_error_telegram_response))
        service = TelegramService()
        result = service.get_foreca_image()
        assert result is None

    def test_invalid_image_object_telegram_response_response_get_foreca_image(self, mocker):
        mocker.patch.object(requests, 'get', return_value=MockResponse(MockReponse.mock_image_object_telegram_response))
        service = TelegramService()
        result = service.get_foreca_image()
        assert result is None

    def test_invalid_telegram_response_telegram_response_response_get_foreca_image(self, mocker):
        mocker.patch.object(requests, 'get', return_value=MockResponse(MockReponse.mock_invalid_telegram_response))
        service = TelegramService()
        result = service.get_foreca_image()
        assert result is None






