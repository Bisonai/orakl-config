"""Tests for generate-configs.py (no network: API responses are mocked).

Run from the repo root:  python3 -m unittest discover -s script
"""
import importlib.util
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

_spec = importlib.util.spec_from_file_location(
    "generate_configs", Path(__file__).with_name("generate-configs.py"))
gc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gc)


def symbols(loader, payload):
    with mock.patch.object(gc, "load_json_from_url", return_value=payload):
        return loader("http://unused")


class StatusFilterTest(unittest.TestCase):
    def test_bingx_requires_status_1(self):
        payload = {"data": {"symbols": [
            {"symbol": "BTC-USDT", "status": 1, "apiStateBuy": True, "apiStateSell": True},
            # delisted pairs stay listed: status 0, apiState* still true
            {"symbol": "XMR-USDT", "status": 0, "apiStateBuy": True, "apiStateSell": True},
            {"symbol": "FOO-USDT", "status": 25, "apiStateBuy": True, "apiStateSell": True},
            {"symbol": "BAR-USDT", "status": 1, "apiStateBuy": False, "apiStateSell": True},
        ]}}
        self.assertEqual(symbols(gc.get_bingx_symbols, payload), ["btcusdt"])

    def test_bitget_requires_online(self):
        payload = {"data": [
            {"symbol": "BTCUSDT", "status": "online"},
            {"symbol": "HOTUSDT", "status": "offline"},
            {"symbol": "RUNEUSDT", "status": "halt"},
        ]}
        self.assertEqual(symbols(gc.get_bitget_symbols, payload), ["btcusdt"])

    def test_okx_requires_live_spot(self):
        payload = {"data": [
            {"instType": "SPOT", "state": "live", "baseCcy": "BTC", "quoteCcy": "USDT"},
            {"instType": "SPOT", "state": "suspend", "baseCcy": "JST", "quoteCcy": "USDT"},
            {"instType": "SPOT", "state": "preopen", "baseCcy": "NEW", "quoteCcy": "USDT"},
            {"instType": "SWAP", "state": "live", "baseCcy": "ETH", "quoteCcy": "USDT"},
        ]}
        self.assertEqual(symbols(gc.get_okx_symbols, payload), ["btcusdt"])

    def test_bybit_v5_requires_trading(self):
        payload = {"result": {"list": [
            {"symbol": "BTCUSDT", "status": "Trading"},
            {"symbol": "NEWUSDT", "status": "PreLaunch"},
        ]}}
        self.assertEqual(symbols(gc.get_bybit_symbols, payload), ["btcusdt"])

    def test_gateio_requires_tradable(self):
        payload = [
            {"id": "BTC_USDT", "trade_status": "tradable"},
            {"id": "OLD_USDT", "trade_status": "untradable"},
        ]
        self.assertEqual(symbols(gc.get_gateio_symbols, payload), ["btcusdt"])

    def test_crypto_requires_tradable(self):
        payload = {"result": {"data": [
            {"symbol": "BTC_USDT", "tradable": True},
            {"symbol": "OLD_USDT", "tradable": False},
        ]}}
        self.assertEqual(symbols(gc.get_crypto_symbols, payload), ["btcusdt"])

    def test_btse_requires_active(self):
        payload = [
            {"symbol": "BTC-USDT", "isMarketOpenToSpot": True, "active": True},
            {"symbol": "OLD-USDT", "isMarketOpenToSpot": True, "active": False},
        ]
        self.assertEqual(symbols(gc.get_btse_symbols, payload), ["btcusdt"])

    def test_xt_requires_online(self):
        payload = {"result": {"symbols": [
            {"symbol": "btc_usdt", "state": "ONLINE", "tradingEnabled": True, "openapiEnabled": True},
            {"symbol": "old_usdt", "state": "OFFLINE", "tradingEnabled": True, "openapiEnabled": True},
        ]}}
        self.assertEqual(symbols(gc.get_xt_symbols, payload), ["btcusdt"])

    def test_no_coinex_loader(self):
        self.assertNotIn("coinex", gc.SYMBOL_LOADERS)


class StoreSymbolsTest(unittest.TestCase):
    def test_failing_provider_is_skipped(self):
        def boom(url):
            raise RuntimeError("unreachable")
        loaders = {"good": lambda url: ["btcusdt"], "bad": boom}
        with tempfile.TemporaryDirectory() as d:
            urls_path = os.path.join(d, "urls.json")
            out = os.path.join(d, "tmp", "symbols.json")
            with open(urls_path, "w") as f:
                json.dump({"good": "u1", "bad": "u2"}, f)
            with mock.patch.object(gc, "SYMBOL_LOADERS", loaders), \
                    mock.patch("sys.stderr"), mock.patch("builtins.print"):
                gc.store_symbols(urls_path, out)
            with open(out) as f:
                self.assertEqual(json.load(f), {"good": ["btcusdt"]})


class CacheTest(unittest.TestCase):
    def test_staleness(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "symbols.json")
            self.assertTrue(gc.symbols_cache_is_stale(p))
            open(p, "w").close()
            self.assertFalse(gc.symbols_cache_is_stale(p))
            old = time.time() - (gc.SYMBOLS_MAX_AGE_HOURS + 1) * 3600
            os.utime(p, (old, old))
            self.assertTrue(gc.symbols_cache_is_stale(p))


class ReplaceConfigTest(unittest.TestCase):
    def test_keeps_feeds_of_unavailable_providers(self):
        prev = {
            "name": "BTC-USDT", "fetchInterval": 1, "aggregateInterval": 2, "submitInterval": 3,
            "feeds": [
                {"name": "naver-BTC-USDT", "definition": {"url": "x"}},
                gc.make_wss_object("bitmart", "btc", "usdt"),
                gc.make_wss_object("bingx", "btc", "usdt"),
            ],
        }
        new_feeds = [gc.make_wss_object("binance", "btc", "usdt")]
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "BTC-USDT.json"), "w") as f:
                json.dump(prev, f)
            gc.replace_config_file(d, "BTC-USDT", new_feeds, {"binance", "bingx"})
            with open(os.path.join(d, "BTC-USDT.json")) as f:
                names = [x["name"] for x in json.load(f)["feeds"]]
        # bingx loaded and no longer lists the pair -> removed;
        # bitmart failed to load -> kept
        self.assertEqual(names, ["naver-BTC-USDT", "bitmart-wss-BTC-USDT", "binance-wss-BTC-USDT"])


if __name__ == "__main__":
    unittest.main()
