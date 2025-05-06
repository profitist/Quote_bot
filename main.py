import httpx
import asyncio
from typing import Optional
from Bot import router as rt
from database.models import init_db
import Bot.sender as sender


BOT_TOKEN = '7355825443:AAEHx531DYZcgxD91YyLjW09z-LucAXOk10'

BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'
offset = 0


async def main() -> None:
    global offset
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        while True:
            updates = await sender.get_updates(client, offset)
            if not updates:
                continue
            offset = updates[-1]['update_id'] + 1
            await process_updates(updates, client)


async def process_updates(data: Optional[list], client: httpx.AsyncClient) -> None:
    for update in data:
        print('Сообщение отправлено')
        await rt.process_request(update, client)


if __name__ == '__main__':
    try:
        init_db()
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')