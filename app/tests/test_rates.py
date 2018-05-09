import asyncio
import unittest
from aioresponses import aioresponses

from app.rates import RatesProvider, ProviderError
from .utils import config, mock_fixerio_responce


loop = asyncio.get_event_loop()


class RatesProviderTestCase(unittest.TestCase):
    def setUp(self):
        self.provider = RatesProvider(config.fixerio_api_key, config.symbols)

    @aioresponses()
    def testProviderError(self, mocked):
        with self.assertRaises(ProviderError):
            mocked.get('http://data.fixer.io/api/latest?symbols=ONE,TWO&access_key=test_api_key', status=500)
            loop.run_until_complete(self.provider.update())

    @aioresponses()
    def testProvider(self, mocked):
        mock_fixerio_responce(mocked)
        loop.run_until_complete(self.provider.update())

        self.assertIn('EUR', self.provider.rates)
        self.assertIn('ONE', self.provider.rates)
        self.assertIn('TWO', self.provider.rates)

        self.assertIn('EUR', self.provider.rates['ONE'])
        self.assertIn('TWO', self.provider.rates['ONE'])

        self.assertEqual(self.provider.rates['ONE']['EUR'], 0.2)
        self.assertEqual(self.provider.rates['ONE']['TWO'], 20)

        self.assertIn('EUR', self.provider.symbol_names)
        self.assertIn('ONE', self.provider.symbol_names)
        self.assertIn('TWO', self.provider.symbol_names)

        self.assertEqual(self.provider.symbol_names['EUR'], 'Euro')
        self.assertEqual(self.provider.symbol_names['ONE'], 'One')
        self.assertEqual(self.provider.symbol_names['TWO'], 'Two')
