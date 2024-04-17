from seleniumwire import webdriver
import time
from fake_useragent import UserAgent
from PIL import Image
from io import BytesIO
import os
import base64


class SeleniumForecaManager:
    def __init__(self):

        # options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")

        # user-agent
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.binary_location = ''

        # change useragent
        useragent = UserAgent()

        self.options.add_argument(f"user-agent={useragent.random}")

    def get_image(self) -> bytes:
        try:
            driver = webdriver.Chrome(options=self.options)

            url = "https://www.foreca.ru/Russia/Rostov-na-Donu"
            print('get url: ', url)
            driver.get(url)
            print('resize window')
            driver.set_window_size(1024, 1200)
            print('screenshot')
            screenshot = BytesIO(driver.get_screenshot_as_png())

            print('preparing screenshot from page')

            img = Image.open(screenshot, mode='r')
            print('crop')
            new_img = img.crop((265, 500, 980, 1140,))

            screenshot_path = os.getcwd() + '/page.png'
            print('save to bytes')

            img_byte_arr = BytesIO()
            new_img.save(img_byte_arr, format='PNG')
            img_byte_arr: bytes = base64.b64encode(img_byte_arr.getvalue())

            return img_byte_arr
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
