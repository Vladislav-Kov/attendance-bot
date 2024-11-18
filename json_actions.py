import json
import aiofiles
from config import SESSIONS_JSON_PATH
import logging

from logger import configure_logging

logger = logging.getLogger(__name__)
configure_logging(logging.DEBUG)


async def get_json_data() -> dict:
    logger.debug("get_json_data - start")

    try:
        async with aiofiles.open(SESSIONS_JSON_PATH, 'r') as file:
            content = await file.read()
            data = json.loads(content)
    except FileNotFoundError:
        with open(SESSIONS_JSON_PATH, 'w') as file:
            data = {}
            js_data = json.dumps(data)
            file.write(js_data)

    logger.info("data out - %s", data)
    logger.debug("get_json_data - finish")
    return data


async def set_json_data(data: dict):
    logger.debug("set_json_data - start")
    logger.info("data in - %s", data)

    js_data = json.dumps(data)
    async with aiofiles.open(SESSIONS_JSON_PATH, 'w') as file:
        await file.write(js_data)

    logger.debug("set_json_data - finish")