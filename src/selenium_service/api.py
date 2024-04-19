import logging

from fastapi import FastAPI
from pydantic import ValidationError

from models import SeleniumApiImageResponse, SeleniumApiForecaImage, SeleniumApiErrorResponse
from selenium_service import SeleniumService

app = FastAPI()
service = SeleniumService()


@app.get("/")
async def get_image() -> SeleniumApiImageResponse | SeleniumApiErrorResponse:
    try:
        data: SeleniumApiForecaImage = service.get_foreca_image()

        if data and data.image_base64:
            return SeleniumApiImageResponse(image=data.model_dump())

        return SeleniumApiErrorResponse(success=False, error_message="No image")
    
    except ValidationError as err:
        logging.error(err.json())
        return SeleniumApiErrorResponse(success=False, error_message="No image")
    except Exception as err:
        logging.error(err, exc_info=True)
