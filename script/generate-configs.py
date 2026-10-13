import json
import requests
import argparse
import os
import sys
import time
from pathlib import Path

URLS_PATH = Path("script/urls.json")
SYMBOLS_PATH = Path("tmp/symbols.json")
# Cached symbols older than this are refetched: a stale cache re-adds pairs
# that have since been delisted or taken offline.
SYMBOLS_MAX_AGE_HOURS = 24

DEFAULT_FETCH_INTERVAL = 2000
DEFAULT_AGGREGATE_INTERVAL = 400
DEFAULT_SUBMIT_INTERVAL = 60000 # 1 minute

filter_outs = {
    "bitmart": ["joyusdt"],
    "bitget": ["joyusdt"],
    "huobi": ["joyusdt"]
}

def load_json_from_url(url):
    response = requests.get(url=url, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, timeout=30)
    response.raise_for_status()
    json_data = response.json()
    return json_data

def load_json_from_path(file_path: Path):
    with open(file_path) as json_file:
        return json.load(json_file)

def get_binance_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    symbols = json_data["symbols"]
    for entry in symbols:
        if entry["status"] != "TRADING":
            continue
        result.append(entry["symbol"].lower())
    return result


# HashKey Global's exchangeInfo is Binance-format (a "symbols" array whose
# entries carry a "status" of "TRADING"), so the parsing matches binance.
def get_hashkey_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    symbols = json_data["symbols"]
    for entry in symbols:
        if entry["status"] != "TRADING":
            continue
        result.append(entry["symbol"].lower())
    return result

def get_coinbase_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data:
        if entry["trading_disabled"]:
            continue
        result.append(entry["id"].replace("-", "").lower())
    return result

def get_kucoin_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]:
        if entry["enableTrading"] == False:
            continue
        result.append(entry["symbol"].replace("-","").lower())
    return result

def get_bybit_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    # v5 instruments-info; spot is not paginated. status: Trading | PreLaunch | ...
    for entry in json_data["result"]["list"]:
        if entry.get("status") != "Trading":
            continue
        result.append(entry["symbol"].lower())
    return result

def get_bistamp_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data:
        result.append(entry["pair"].replace("/","").lower())
    return result

def get_gemini_symbols(url):
    return load_json_from_url(url)

def get_upbit_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data:
        raw = entry["market"].split("-")
        if len(raw) != 2:
            continue
        base = raw[1]
        quote = raw[0]
        result.append(f"{base}{quote}".lower())
    return result

def get_korbit_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for key, _ in json_data["exchange"].items():
        result.append(key.replace("_","").lower())
    return result

def get_crypto_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["result"]["data"]:
        if not entry.get("tradable", False):
            continue
        result.append(entry["symbol"].replace("_","").lower())
    return result

def get_btse_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data:
        if not entry["isMarketOpenToSpot"] or not entry.get("active", False):
            continue
        result.append(entry["symbol"].replace("-","").lower())
    return result

def get_bithumb_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for key in json_data["data"].keys():
        result.append(f'{key}krw'.lower())
    return result

def get_gateio_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data:
        if entry.get("trade_status") != "tradable":
            continue
        result.append(entry["id"].replace("_","").lower())
    return result

def get_lbank_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]:
        result.append(entry.replace("_",""))
    return result

def get_bitget_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]:
        # status: online | offline | halt
        if entry.get("status") != "online":
            continue
        result.append(entry["symbol"].lower())
    return result

def get_coinone_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["markets"]:
        if entry["trade_status"] != 1 or "market" not in entry["order_types"]:
            continue
        result.append(entry["target_currency"].lower() + entry["quote_currency"].lower())
    return result

def get_huobi_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]:
        if entry["state"] != "online":
            continue
        result.append(entry["symbol"])
    return result

def get_mexc_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]:
        result.append(entry.lower())
    return result

def get_okx_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]:
        # state: live | suspend | preopen
        if entry["instType"] != "SPOT" or entry.get("state") != "live":
            continue
        result.append(entry["baseCcy"].lower() + entry["quoteCcy"].lower())
    return result

def get_kraken_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for key, value in json_data["result"].items():
        if value["status"] != "online":
            continue
        result.append(key.lower())
    return result

def get_bingx_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]["symbols"]:
        # status: 1 = online; 0 = offline (delisted pairs stay listed with
        # status 0 and apiState* still true), other values = not trading
        if entry.get("status") != 1 or not entry["apiStateSell"] or not entry["apiStateBuy"]:
            continue
        result.append(entry["symbol"].replace("-","").lower())
    return result

def get_bitmart_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]["symbols"]:
        result.append(entry.replace("_","").lower())
    return result

def get_xt_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["result"]["symbols"]:
        if entry.get("state") != "ONLINE" or not entry["tradingEnabled"] or not entry["openapiEnabled"]:
            continue
        result.append(entry["symbol"].replace("_","").lower())
    return result

def get_gopax_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data:
        result.append(entry["name"].replace("-","").lower())
    return result

def get_orangex_symbols(url):
    result = []
    json_data = load_json_from_url(url)

    for entry in json_data["result"]:
        if not entry["is_active"]:
            continue
        result.append(entry["show_name"].replace("/","").lower())
    return result

SYMBOL_LOADERS = {
    "binance": get_binance_symbols,
    "coinbase": get_coinbase_symbols,
    "kucoin": get_kucoin_symbols,
    "bybit": get_bybit_symbols,
    "bitstamp": get_bistamp_symbols,
    "gemini": get_gemini_symbols,
    "upbit": get_upbit_symbols,
    "korbit": get_korbit_symbols,
    "crypto": get_crypto_symbols,
    "btse": get_btse_symbols,
    "bithumb": get_bithumb_symbols,
    "gateio": get_gateio_symbols,
    "lbank": get_lbank_symbols,
    "bitget": get_bitget_symbols,
    "coinone": get_coinone_symbols,
    "huobi": get_huobi_symbols,
    "mexc": get_mexc_symbols,
    "okx": get_okx_symbols,
    "kraken": get_kraken_symbols,
    "bingx": get_bingx_symbols,
    "bitmart": get_bitmart_symbols,
    "xt": get_xt_symbols,
    "gopax": get_gopax_symbols,
    "orangex": get_orangex_symbols,
    "hashkey": get_hashkey_symbols,
}

def store_symbols(urls_path, symbols_path):
    # A provider whose API fails is left out of the cache (with a warning)
    # instead of aborting the run; see replace_config_file for how its
    # existing feeds are kept.
    store_directory = os.path.dirname(symbols_path)
    if not os.path.exists(store_directory):
        os.makedirs(store_directory)

    result = {}
    failed = []
    urls = load_json_from_path(urls_path)

    for provider, loader in SYMBOL_LOADERS.items():
        try:
            result[provider] = loader(urls[provider])
        except Exception as e:
            failed.append(provider)
            print(f"WARNING: {provider} symbols not loaded, skipping: {e!r}", file=sys.stderr)
            continue
        print(f"{provider} symbol loaded")

    if failed:
        print(f"WARNING: no symbols for {', '.join(failed)}; their feeds are neither added nor removed", file=sys.stderr)

    with open(symbols_path, "w") as f:
        json.dump(result, f, indent=4)

def symbols_cache_is_stale(symbols_path, max_age_hours=SYMBOLS_MAX_AGE_HOURS):
    if not os.path.exists(symbols_path):
        return True
    return time.time() - os.path.getmtime(symbols_path) > max_age_hours * 3600

def make_wss_object(provider, base, quote):
    wsFeed = {}
    wsFeed["name"] = f"{provider}-wss-{base.upper()}-{quote.upper()}"
    wsFeed["definition"] = {}
    wsFeed["definition"]["type"] = "wss"
    wsFeed["definition"]["provider"] = provider
    wsFeed["definition"]["base"] = base.upper()
    wsFeed["definition"]["quote"] = quote.upper()
    return wsFeed

def is_supported(symbol_list, base, quote):

    for symbol in symbol_list:
        if symbol == f"{base}{quote}".lower():
            return True
    return False

def get_all_supported_providers(possible_symbols, base, quote):
    supported_providers = []
    for key, value in possible_symbols.items():
        if filter_outs.get(key) is not None and f"{base}{quote}".lower() in filter_outs.get(key):
            continue
        if is_supported(value, base, quote):
            supported_providers.append(key)
    return supported_providers

def load_existing_symbols(folder_path):
    result = []
    postfix = ".json"
    if not os.path.exists(folder_path):
        return []
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)) and \
            os.path.splitext(filename)[-1] == ".json":
            result.append(filename[:-len(postfix)])

    return result

def load_args():
    parser = argparse.ArgumentParser(description="Generate config files, it'll try to update existing config files, generate config file if not exist")

    parser.add_argument("--onlysymbols", type=bool, default=False, help="Will only reload symbols from each exchanges")
    parser.add_argument("--refresh", type=bool, default=False, help="Refresh supported symbols from apis, true or false")
    parser.add_argument("--symbols", type=str, default="", required=False, help="configs to create, separated by comma, ex) btc-usdt, eth-usdt...")
    parser.add_argument("--network", type=str, default="kairos", choices=["mainnet", "kairos"], required=False, help="network to generate, defaults to kairos")
    parser.add_argument("--replace", type=bool, default=False, required=False, help="remove old ws sources and add new ones")

    args = parser.parse_args()

    return args

def feed_exists(feeds, name):
    for feed in feeds:
        if feed["name"] == name:
            return True
    return False

def update_or_make_config_file(config_folder_path, symbol, feeds):
    result = {}
    if not os.path.exists(config_folder_path+"/"+symbol+".json"):
        result["name"] = symbol
        result["fetchInterval"] = DEFAULT_FETCH_INTERVAL
        result["aggregateInterval"] = DEFAULT_AGGREGATE_INTERVAL
        result["submitInterval"] = DEFAULT_SUBMIT_INTERVAL
        result["feeds"] = feeds
        with open(f"{config_folder_path}/{symbol}.json", "w") as f:
            json.dump(result, f, indent=4)
        return

    with open(f"{config_folder_path}/{symbol}.json", "r") as f:
        result = json.load(f)

    result["aggregateInterval"] = DEFAULT_AGGREGATE_INTERVAL
    for feed in feeds:
        if not feed_exists(result["feeds"], feed["name"]):
            result["feeds"].append(feed)

    with open(f"{config_folder_path}/{symbol}.json", "w") as f:
        json.dump(result, f, indent=4)

def replace_config_file(config_folder_path, symbol, feeds, available_providers=None):
    # removes all ws feeds from previous file, and replace with new one.
    # ws feeds of providers not in available_providers (symbols failed to
    # load) are kept as-is, since their support is unknown.
    result = {}
    if not os.path.exists(config_folder_path+"/"+symbol+".json"):
        result["name"] = symbol
        result["fetchInterval"] = DEFAULT_FETCH_INTERVAL
        result["aggregateInterval"] = DEFAULT_AGGREGATE_INTERVAL
        result["submitInterval"] = DEFAULT_SUBMIT_INTERVAL
        result["feeds"] = feeds
        with open(f"{config_folder_path}/{symbol}.json", "w") as f:
            json.dump(result, f, indent=4)
        return

    with open(f"{config_folder_path}/{symbol}.json", "r") as f:
        prev = json.load(f)

    result["name"] = symbol
    result["fetchInterval"] = prev["fetchInterval"]
    result["aggregateInterval"] = prev["aggregateInterval"]
    result["submitInterval"] = prev["submitInterval"]
    result["feeds"] = []
    for feed in prev["feeds"]:
        provider = feed.get("definition", {}).get("provider")
        if "-wss-" not in feed["name"] or \
            (available_providers is not None and provider not in available_providers):
            result["feeds"].append(feed)

    for feed in feeds:
        result["feeds"].append(feed)



    with open(f"{config_folder_path}/{symbol}.json", "w") as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    args = load_args()

    symbols_only = args.onlysymbols
    refresh = args.refresh
    input_symbols = args.symbols.replace(" ","").split(",")
    network = args.network
    is_replace = args.replace

    if refresh or symbols_only:
        store_symbols(URLS_PATH, SYMBOLS_PATH)
    elif symbols_cache_is_stale(SYMBOLS_PATH):
        if os.path.exists(SYMBOLS_PATH):
            print(f"{SYMBOLS_PATH} is older than {SYMBOLS_MAX_AGE_HOURS}h, refreshing")
        store_symbols(URLS_PATH, SYMBOLS_PATH)

    if symbols_only:
        exit(0)

    possible_symbols = load_json_from_path(SYMBOLS_PATH)

    work_symbols = []
    for symbol in input_symbols:
        if len(symbol.split("-")) != 2:
            continue
        work_symbols.append(symbol)

    existing_symbols = load_existing_symbols(Path(f"config/{network}"))
    work_symbols.extend(existing_symbols)

    result = {}
    for symbol in work_symbols:
        base = symbol.split("-")[0]
        quote = symbol.split("-")[1]
        providers = get_all_supported_providers(possible_symbols, base, quote)

        wsFeeds = []
        for provider in providers:

            wsFeed = make_wss_object(provider, base, quote)
            wsFeeds.append(wsFeed)

        result[symbol] = wsFeeds



    for symbol, feeds in result.items():
        if is_replace:
            replace_config_file(f"config/{network}", symbol, feeds, set(possible_symbols))
        else:
            update_or_make_config_file(f"config/{network}", symbol, feeds)