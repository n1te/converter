from json import loads
from aioresponses import aioresponses
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop, setup_test_loop

from app import App
from .utils import config, mock_fixerio_responce


class AppTestCase(AioHTTPTestCase):
    def setUp(self):
        self.loop = setup_test_loop()

        app = App(config)

        @aioresponses()
        def get_app_with_mocking(mocked):
            mock_fixerio_responce(mocked)
            self.loop.run_until_complete(app.provider.update())

        get_app_with_mocking()

        self.app = app

        self.server = self.loop.run_until_complete(self.get_server(self.app))
        self.client = self.loop.run_until_complete(
            self.get_client(self.server))
        self.loop.run_until_complete(self.client.start_server())
        self.loop.run_until_complete(self.setUpAsync())

    @unittest_run_loop
    async def testIndex(self):
        resp = await self.client.request('GET', '/')
        self.assertEqual(resp.status, 200)
        text = await resp.text()
        self.assertIn('Currency converter', text)

    @unittest_run_loop
    async def testRates(self):
        resp = await self.client.request('GET', '/rates.json')
        self.assertEqual(resp.status, 200)

        text = await resp.text()
        rates = loads(text)

        self.assertIn('EUR', rates)
        self.assertIn('ONE', rates)
        self.assertIn('TWO', rates)
        self.assertIn('EUR', rates['TWO'])
        self.assertIn('ONE', rates['TWO'])
        self.assertEqual(rates['EUR']['ONE'], 5)
        self.assertEqual(rates['TWO']['ONE'], 0.05)
        self.assertEqual(rates['ONE']['TWO'], 20)

    @unittest_run_loop
    async def testSymbols(self):
        resp = await self.client.request('GET', '/symbols.json')
        self.assertEqual(resp.status, 200)

        text = await resp.text()
        symbols = loads(text)

        self.assertIn('EUR', symbols)
        self.assertIn('ONE', symbols)
        self.assertIn('TWO', symbols)

        self.assertEqual(symbols['EUR'], 'Euro')
        self.assertEqual(symbols['ONE'], 'One')
        self.assertEqual(symbols['TWO'], 'Two')
