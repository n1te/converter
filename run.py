import logging
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app import App
from config import config


logging.basicConfig(level=logging.INFO)

app = App(config)


async def app_factory():
    await app.update_rates()
    app.router.add_static('/static/', path='./app/assets/static/')
    return app

scheduler = AsyncIOScheduler()
scheduler.add_job(app.update_rates, 'cron', hour=1)
scheduler.start()

web.run_app(app_factory())
