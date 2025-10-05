import asyncio
from bot.bot import bot, dp
from api.main import app
import uvicorn

async def main():
    asyncio.create_task(dp.start_polling(bot))
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    asyncio.run()