"""Tests for generate-readme.py source labels (#232).

Run from the repo root:  python3 -m unittest discover -s script
"""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "generate_readme", Path(__file__).with_name("generate-readme.py"))
gr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gr)


def wss(name, provider):
    return {"name": name, "definition": {"type": "wss", "provider": provider}}


def pool(name):
    return {"name": name, "definition": {"type": "UniswapPool"}}


class DisplaySourceTest(unittest.TestCase):
    def test_canonical_case(self):
        for prefix, label in [("Daum", "Daum"), ("daum", "Daum"),
                              ("Dragonswap", "DragonSwap"), ("DragonSwap", "DragonSwap"),
                              ("Pancakeswap", "PancakeSwap"), ("naver", "Naver"),
                              ("capybara", "Capybara"), ("KlaySwap", "KlaySwap")]:
            self.assertEqual(gr.display_source(prefix), label, prefix)

    def test_qualifier_stripped(self):
        self.assertEqual(gr.display_source("UniswapV3-0.05"), "UniswapV3")
        self.assertEqual(gr.display_source("uniswapv3-0.3"), "UniswapV3")
        self.assertEqual(gr.display_source("uniswapv3"), "UniswapV3")
        self.assertEqual(gr.display_source("uniswapv4-polygon-005"), "UniswapV4")

    def test_unknown_source_kept(self):
        self.assertEqual(gr.display_source("SomeDex"), "SomeDex")
        self.assertEqual(gr.display_source("SomeDex-1"), "SomeDex")


class SourceNameTest(unittest.TestCase):
    def test_wss_uses_provider_unchanged(self):
        self.assertEqual(gr.source_name(wss("daum:BTC-USDT", "binance")), "binance")

    def test_non_wss_uses_normalized_source(self):
        self.assertEqual(gr.source_name(pool("Dragonswap:KRWO-USDT")), "DragonSwap")
        self.assertEqual(gr.source_name({"name": "daum:KRW-USD"}), "Daum")
        self.assertEqual(gr.source_name(pool("uniswapv3-arbitrum:MYRC-USDT")), "UniswapV3")

    def test_unusable_name(self):
        self.assertIsNone(gr.source_name({"name": ""}))
        self.assertIsNone(gr.source_name({"name": ":X-Y"}))
        self.assertIsNone(gr.source_name({}))


class LoadPairTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "ETH-USDT.json"

    def tearDown(self):
        self._tmp.cleanup()

    def sources(self, *feeds):
        self.path.write_text(json.dumps({
            "name": "ETH-USDT", "fetchInterval": 2000, "aggregateInterval": 400,
            "submitInterval": 15000, "feeds": list(feeds)}))
        return gr.load_pair(self.path)[1]

    def test_dedupes_after_normalization(self):
        self.assertEqual(
            self.sources(wss("binance-wss:ETH-USDT", "binance"),
                         pool("uniswapv3-0.05:ETH-USDT"), pool("uniswapv3-0.3:ETH-USDT"),
                         pool("Dragonswap:ETH-USDT"), pool("DragonSwap:ETH-USDT"),
                         {"name": "daum:ETH-USD"}, {"name": "Daum:ETH-USD"}),
            ["binance", "Daum", "DragonSwap", "UniswapV3"])

    def test_unknown_prefix_case_variants_deduped(self):
        self.assertEqual(self.sources(pool("FooDex:ETH-USDT"), pool("foodex:ETH-USDT")),
                         ["FooDex"])

    def test_malformed_outside_repo_warns(self):
        self.path.write_text("not json")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertIsNone(gr.load_pair(self.path))
        # full path normally; relative if TMPDIR is inside the repo
        self.assertIn("ETH-USDT.json: could not read/parse JSON", err.getvalue())


if __name__ == "__main__":
    unittest.main()
