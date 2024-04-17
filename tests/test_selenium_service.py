import pytest
from pydantic_core._pydantic_core import ValidationError

from src.selenium_service.cache_manager import SeleniumCacheManager
from src.selenium_service.selenium_service import SeleniumService
from src.selenium_service.foreca import SeleniumForecaManager
from src.selenium_service.models import SeleniumApiForecaImage, SeleniumApiResponse


class MockSeleniumCacheManager(SeleniumCacheManager):
    def get_foreca_image(self) -> SeleniumApiForecaImage:
        return SeleniumApiForecaImage(
                name='test',
                image_base64=b'any mock bytes'
            )

    def save_foreca_image(self, data: SeleniumApiForecaImage):
        pass


class TestSeleniumService:
    @pytest.fixture(scope='function')
    def mocking_setup(self, mocker):
        mocker.patch.object(SeleniumCacheManager, 'save_foreca_image', return_value=None)

    def test_success_get_foreca_image(self, mocker, mocking_setup):
        mocker.patch.object(
            SeleniumCacheManager,
            'get_foreca_image',
            return_value=SeleniumApiForecaImage(
                name='test',
                image_base64=b'any mock bytes'
            )
        )
        selenium_service = SeleniumService()
        result = selenium_service.get_foreca_image()
        assert isinstance(result, SeleniumApiForecaImage)

    def test_return_invalid_data_from_cache_get_foreca_image(self, mocker, mocking_setup):
        mocker.patch.object(
            SeleniumCacheManager,
            'get_foreca_image',
            return_value=SeleniumApiForecaImage(
                name='test',
                image_base64=b''
            )
        )
        mocker.patch.object(SeleniumForecaManager, 'get_image', return_value=None)
        selenium_service = SeleniumService()
        assert selenium_service.get_foreca_image() is None

    def test_success_save_foreca_image_to_cache(self, mocker, mocking_setup):
        mocker.patch.object(
            SeleniumForecaManager,
            'get_image',
            return_value=b'any asdasdasd mock bytes'
        )
        selenium_service = SeleniumService()
        assert isinstance(selenium_service._save_foreca_image_to_cache(), SeleniumApiForecaImage)

    def test_invalid_received_data_save_foreca_image_to_cache(self, mocker, mocking_setup):
        mocker.patch.object(
            SeleniumForecaManager,
            'get_image',
            return_value=b''
        )
        selenium_service = SeleniumService()
        assert selenium_service._save_foreca_image_to_cache() is None
