from asyncio import run
from loguru import logger

from app.app import create_app
from app.config import Config


async def main(config: Config):
    bot, dp = await create_app(config)
    logger.info('Running the app...')
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    run(main(Config()))
