import logging
from aiohttp import web
from app.rates import RatesProvider, ProviderError


async def index_handler(request):
    with open('app/assets/index.html') as index_file:
        resp = web.Response(body=index_file.read())
        resp.headers['content-type'] = 'text/html'
        return resp


async def rates_handler(request):
    return web.json_response(request.app.provider.rates)


async def symbols_handler(request):
    return web.json_response(request.app.provider.symbol_names)


class App(web.Application):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = RatesProvider(config.fixerio_api_key, config.symbols)

        self.router.add_routes([
            web.get('/', index_handler),
            web.get('/rates.json', rates_handler),
            web.get('/symbols.json', symbols_handler)
        ])

    async def update_rates(self):
        logging.info('Updatind rates...')
        try:
            await self.provider.update()
        except ProviderError as e:
            logging.error('Error: ' + str(e))
        logging.info('Done!')
