import base64
import logging
from io import BytesIO

from PIL import Image
from fake_useragent import UserAgent
from seleniumwire import webdriver

logging.getLogger('seleniumwire.handler').setLevel(logging.WARNING)

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
        self.driver = None

    def get_image(self) -> bytes:
        try:
            logging.info('Start getting image')
            self.driver = webdriver.Chrome(options=self.options)

            url = "https://www.foreca.ru/Russia/Rostov-na-Donu"
            logging.debug('get url: ', url)
            self.driver.get(url)
            logging.debug('resize window')
            self.driver.set_window_size(1024, 1200)
            logging.debug('screenshot')
            screenshot = BytesIO(self.driver.get_screenshot_as_png())

            logging.debug('preparing screenshot from page')

            img = Image.open(screenshot, mode='r')
            logging.debug('crop')
            new_img = img.crop((265, 500, 980, 1140,))

            logging.debug('save to bytes')
            img_byte_arr = BytesIO()
            new_img.save(img_byte_arr, format='PNG')
            img_byte_arr: bytes = base64.b64encode(img_byte_arr.getvalue())

            return img_byte_arr
        except Exception as ex:
            logging.error(ex, exc_info=True)
        finally:
            self.driver.close()
            self.driver.quit()
