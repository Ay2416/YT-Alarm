import asyncio
from aytch import get_channel_info

async def main():
    channel_url = 'your_youtube_link'
    channel_info = await get_channel_info(channel_url)
    print(channel_info['author_id'])

asyncio.run(main())