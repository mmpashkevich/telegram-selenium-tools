from fastapi import FastAPI

from selenium_service import SeleniumService
from pydantic import ValidationError
from models import SeleniumApiImageResponse, SeleniumApiForecaImage, SeleniumApiErrorResponse
import sys

app = FastAPI()
service = SeleniumService()


@app.get("/")
async def get_image() -> SeleniumApiImageResponse | SeleniumApiErrorResponse:
    try:
        data: SeleniumApiForecaImage = service.get_foreca_image()

        if data and data.image_base64:
            return SeleniumApiImageResponse(image=data)

        return SeleniumApiErrorResponse(success=False, error_message="No image")
    
    except ValidationError as err:
        print(err.json())
        return SeleniumApiErrorResponse(success=False, error_message="No image")

