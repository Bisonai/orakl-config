"""Tests for collect-files.py --check (semantic bundle check, #260).

Run from the repo root:  python3 -m unittest discover -s script
"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "collect_files", Path(__file__).with_name("collect-files.py"))
cf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cf)


def feed(name, provider="binance"):
    return {"name": name, "definition": {"type": "wss", "provider": provider}}


def pair(name, *feeds, submit=15000):
    return {"name": name, "fetchInterval": 2000, "submitInterval": submit, "feeds": list(feeds)}


class CheckBundleTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "src").mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def check(self, sources, bundle):
        for i, src in enumerate(sources):
            text = src if isinstance(src, str) else json.dumps(src, indent=2)
            (self.root / "src" / f"{i:03}.json").write_text(text)
        (self.root / "bundle.json").write_text(bundle if isinstance(bundle, str) else json.dumps(bundle, indent=4))
        return cf.check_bundle(Path("src"), Path("bundle.json"), self.root)

    def test_match_ignores_entry_order_and_key_order(self):
        a, b = pair("A-USDT", feed("x"), feed("y")), pair("B-USDT", feed("z"))
        reordered_b = {k: b[k] for k in reversed(list(b))}
        self.assertEqual(self.check([a, b], [reordered_b, a]), [])

    def test_missing_and_extra_pair(self):
        errors = self.check([pair("A-USDT", feed("x"))], [pair("B-USDT", feed("x"))])
        self.assertEqual(len(errors), 2)
        self.assertIn("A-USDT: in src/ but missing from bundle.json", errors)
        self.assertIn("B-USDT: in bundle.json but not in src/", errors)

    def test_feed_missing_changed_and_reordered(self):
        src = pair("A-USDT", feed("x"), feed("y"), feed("z"))
        com = pair("A-USDT", feed("z"), feed("x", "kucoin"))
        [error] = self.check([src], [com])
        self.assertIn("feed y missing from bundle", error)
        self.assertIn("feed x differs", error)
        self.assertIn("feed order differs", error)

    def test_type_change_detected(self):
        [error] = self.check([pair("A-USDT", feed("x"))], [pair("A-USDT", feed("x"), submit=15000.0)])
        self.assertIn("submitInterval: src/=15000 bundle=15000.0", error)

    def test_duplicate_names(self):
        errors = self.check([pair("A-USDT", feed("x"))], [pair("A-USDT", feed("x")), pair("A-USDT", feed("x"))])
        self.assertIn("bundle.json: duplicate name 'A-USDT'", errors)
        [error] = self.check([pair("B-USDT", feed("x"))], [pair("B-USDT", feed("x"), feed("x"))])
        self.assertIn("duplicate feed names", error)

    def test_malformed_inputs_reported_not_raised(self):
        self.assertIn("cannot load", self.check(['{"name": "A",}'], [])[0])
        self.assertIn("expected a JSON list", self.check([pair("A-USDT")], {"result": [pair("A-USDT")]})[0])
        self.assertIn("expected a JSON list", self.check([{"name": ["A"]}], [])[0])
        [error] = self.check([pair("A-USDT", {"name": {"x": 1}})], [pair("A-USDT")])
        self.assertIn("not a list of objects", error)

    def test_missing_vs_null_key_named(self):
        src = pair("A-USDT", feed("x"))
        com = dict(src, aggregateInterval=None)
        [error] = self.check([src], [com])
        self.assertIn("aggregateInterval: src/=(missing) bundle=null", error)

    def test_nested_key_order_ignored(self):
        src = pair("A-USDT", feed("x"), submit={"a": 1, "b": 2})
        com = pair("A-USDT", feed("x"), submit={"b": 2, "a": 1})
        self.assertEqual(self.check([src], [com]), [])

    def test_missing_source_dir(self):
        (self.root / "bundle.json").write_text("[]")
        self.assertEqual(cf.check_bundle(Path("nope"), Path("bundle.json"), self.root),
                         ["nope/: source directory not found"])


if __name__ == "__main__":
    unittest.main()
