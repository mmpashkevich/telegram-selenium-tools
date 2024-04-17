from typing import Optional
from pydantic import BaseModel


class SeleniumApiForecaImage(BaseModel):
    name: str
    url: Optional[str] = None
    image_base64: bytes


class SeleniumApiResponse(BaseModel):
    success: bool = True


class SeleniumApiErrorResponse(SeleniumApiResponse):
    success: bool = False
    error_message: str


class SeleniumApiImageResponse(SeleniumApiResponse):
    image: SeleniumApiForecaImage

