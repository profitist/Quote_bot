import httpx
import asyncio
from typing import Optional
from Bot import router as rt
from database.models import init_db
import Bot.sender as sender
from dotenv import dotenv_values


BOT_TOKEN = dotenv_values(".env").get("BOT_TOKEN")
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'
offset = 0


async def main() -> None:
    global offset
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        while True:
            updates = await sender.get_updates(client, offset)
            if updates is None:
                await asyncio.sleep(5)
            offset = updates[-1]['update_id'] + 1
            await process_updates(updates, client)


async def process_updates(data: Optional[list], client: httpx.AsyncClient) -> None:
    for update in data:
        await rt.process_request(update, client)


if __name__ == '__main__':
    try:
        init_db()
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')