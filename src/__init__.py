import logging
import os

level = os.getenv('LOG_LEVEL', 'INFO')

cyan = "\x1b[36;20m"
reset = "\x1b[0m"

fmt = f'{cyan}%(asctime)s | %(levelname)s {reset}| %(message)s | {cyan}(%(filename)s:%(lineno)d){reset}'

logging.basicConfig(level=level, format=fmt)
logging.info(f'Logger configured')
