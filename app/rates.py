from aiohttp import ClientSession
from json import loads


class ProviderError(Exception):
    pass


class RatesProvider(object):
    _base_url = 'http://data.fixer.io/api/'
    _rates = None
    _symbol_names = {}

    def __init__(self, api_key, symbols):
        self._api_key = api_key
        self._symbols = symbols

    async def _make_request(self, method, params=None):
        if params is None:
            params = {}
        params['access_key'] = self._api_key
        async with ClientSession() as session:
            url = '{base}{method}'.format(base=self._base_url, method=method)
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    raise ProviderError('Can`t get data from fixer.io')
                return loads(await resp.text())

    async def _update_symbols(self):
        resp = await self._make_request('symbols')
        self._symbol_names['EUR'] = resp['symbols']['EUR']
        for s in self._symbols:
            self._symbol_names[s] = resp['symbols'][s]

    async def _update_rates(self):
        params = {'symbols': ','.join(self._symbols)}
        fixerio_rates = await self._make_request('latest', params)

        rates = {'EUR': fixerio_rates['rates']}
        for symbol in self._symbols:
            """
            Calculating other rates from EUR because fixer.io provides only EUR_XXX rates on free tariff
            """
            eur_rate = 1 / rates['EUR'][symbol]
            rates[symbol] = dict([(s, eur_rate * rates['EUR'][s]) for s in self._symbols if s != symbol])
            rates[symbol]['EUR'] = eur_rate

        self._rates = rates

    async def update(self):
        await self._update_rates()
        await self._update_symbols()

    @property
    def rates(self):
        return self._rates

    @property
    def symbol_names(self):
        return self._symbol_names
