import json
import aiofiles
from config import SESSIONS_JSON_PATH


async def get_json_data() -> dict:
    try:
        async with aiofiles.open(SESSIONS_JSON_PATH, 'r') as file:
            content = await file.read()
            data = json.loads(content)
    except FileNotFoundError:
        with open(SESSIONS_JSON_PATH, 'w') as file:
            data = {"id":[]}
            js_data = json.dumps(data)
            file.write(js_data)

    return data


async def set_json_data(data: dict):
    js_data = json.dumps(data)
    async with aiofiles.open(SESSIONS_JSON_PATH, 'w') as file:
        await file.write(js_data)