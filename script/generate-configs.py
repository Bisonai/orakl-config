import json
import requests
import argparse
import os
from pathlib import Path

URLS_PATH = Path("script/urls.json")
SYMBOLS_PATH = Path("tmp/symbols.json")

DEFAULT_FETCH_INTERVAL = 2000
DEFAULT_AGGREGATE_INTERVAL = 400
DEFAULT_SUBMIT_INTERVAL = 60000 # 1 minute

filter_outs = {
    "bitmart": ["joyusdt"],
    "coinex": ["joyusdt"],
    "bitget": ["joyusdt"],
    "huobi": ["joyusdt"]
}

def load_json_from_url(url):
    response = requests.get(url=url, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
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
    print("loaded bybit json data")
    for entry in json_data["result"]["list"]:
        if entry["showStatus"] != "1":
            continue
        result.append(entry["name"].lower())
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
        result.append(entry["symbol"].replace("_","").lower())
    return result

def get_btse_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data:
        if not entry["isMarketOpenToSpot"]:
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
        result.append(entry["id"].replace("_","").lower())
    return result

def get_lbank_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]:
        result.append(entry.replace("_",""))
    return result

def get_coinex_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]:
        result.append(entry.lower())
    return result

def get_bitget_symbols(url):
    result = []
    json_data = load_json_from_url(url)
    for entry in json_data["data"]:
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
        if entry["instType"] != "SPOT":
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
        if not entry["apiStateSell"] or not entry["apiStateBuy"]:
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
        if not entry["tradingEnabled"] or not entry["openapiEnabled"]:
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

def store_symbols(urls_path, symbols_path):
    store_directory = os.path.dirname(symbols_path)
    if not os.path.exists(store_directory):
        os.makedirs(store_directory)

    result = {}
    urls = load_json_from_path(urls_path)

    result["binance"] = get_binance_symbols(urls["binance"])
    print("binance symbol loaded")

    result["coinbase"] = get_coinbase_symbols(urls["coinbase"])
    print("coinbase symbol loaded")

    result["kucoin"] = get_kucoin_symbols(urls["kucoin"])
    print("kucoin symbol loaded")

    result["bybit"] = get_bybit_symbols(urls["bybit"])
    print("bybit symbol loaded")

    result["bitstamp"] = get_bistamp_symbols(urls["bitstamp"])
    print("bitstamp symbol loaded")

    result["gemini"] = get_gemini_symbols(urls["gemini"])
    print("gemini symbol loaded")

    result["upbit"] = get_upbit_symbols(urls["upbit"])
    print("upbit symbol loaded")

    result["korbit"] = get_korbit_symbols(urls["korbit"])
    print("korbit symbol loaded")

    result["crypto"] = get_crypto_symbols(urls["crypto"])
    print("crypto symbol loaded")

    result["btse"] = get_btse_symbols(urls["btse"])
    print("btse symbol loaded")

    result["bithumb"] = get_bithumb_symbols(urls["bithumb"])
    print("bithumb symbol loaded")

    result["gateio"] = get_gateio_symbols(urls["gateio"])
    print("gateio symbol loaded")

    result["lbank"] = get_lbank_symbols(urls["lbank"])
    print("lbank symbol loaded")

    result["coinex"] = get_coinex_symbols(urls["coinex"])
    print("coinex symbol loaded")

    result["bitget"] = get_bitget_symbols(urls["bitget"])
    print("bitget symbol loaded")

    result["coinone"] = get_coinone_symbols(urls["coinone"])
    print("coinone symbol loaded")

    result["huobi"] = get_huobi_symbols(urls["huobi"])
    print("huobi symbol loaded")

    result["mexc"] = get_mexc_symbols(urls["mexc"])
    print("mexc symbol loaded")

    result["okx"] = get_okx_symbols(urls["okx"])
    print("okx symbol loaded")

    result["kraken"] = get_kraken_symbols(urls["kraken"])
    print("kraken symbol loaded")

    result["bingx"] = get_bingx_symbols(urls["bingx"])
    print("bingx symbol loaded")

    result["bitmart"] = get_bitmart_symbols(urls["bitmart"])
    print("bitmart symbol loaded")

    result["xt"] = get_xt_symbols(urls["xt"])
    print("xt symbol loaded")

    result["gopax"] = get_gopax_symbols(urls["gopax"])
    print("gopax symbol loaded")

    result["orangex"] = get_orangex_symbols(urls["orangex"])
    print("orangex symbol loaded")


    with open(symbols_path, "w") as f:
        json.dump(result, f, indent=4)

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
    postfix = ".config.json"
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
    parser.add_argument("--network", type=str, default="baobab", required=False, help="network to generate, defaults to baobab")
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
    if not os.path.exists(config_folder_path+"/"+symbol+".config.json"):
        result["name"] = symbol
        result["fetchInterval"] = DEFAULT_FETCH_INTERVAL
        result["aggregateInterval"] = DEFAULT_AGGREGATE_INTERVAL
        result["submitInterval"] = DEFAULT_SUBMIT_INTERVAL
        result["feeds"] = feeds
        with open(f"{config_folder_path}/{symbol}.config.json", "w") as f:
            json.dump(result, f, indent=4)
        return

    with open(f"{config_folder_path}/{symbol}.config.json", "r") as f:
        result = json.load(f)

    result["aggregateInterval"] = DEFAULT_AGGREGATE_INTERVAL
    for feed in feeds:
        if not feed_exists(result["feeds"], feed["name"]):
            result["feeds"].append(feed)

    with open(f"{config_folder_path}/{symbol}.config.json", "w") as f:
        json.dump(result, f, indent=4)

def replace_config_file(config_folder_path, symbol, feeds):
    # removes all ws feeds from previous file, and replace with new one
    result = {}
    if not os.path.exists(config_folder_path+"/"+symbol+".config.json"):
        result["name"] = symbol
        result["fetchInterval"] = DEFAULT_FETCH_INTERVAL
        result["aggregateInterval"] = DEFAULT_AGGREGATE_INTERVAL
        result["submitInterval"] = DEFAULT_SUBMIT_INTERVAL
        result["feeds"] = feeds
        with open(f"{config_folder_path}/{symbol}.config.json", "w") as f:
            json.dump(result, f, indent=4)
        return

    with open(f"{config_folder_path}/{symbol}.config.json", "r") as f:
        prev = json.load(f)

    result["name"] = symbol
    result["fetchInterval"] = prev["fetchInterval"]
    result["aggregateInterval"] = prev["aggregateInterval"]
    result["submitInterval"] = prev["submitInterval"]
    result["feeds"] = []
    for feed in prev["feeds"]:
        if "-wss-" not in feed["name"]:
            result["feeds"].append(feed)

    for feed in feeds:
        result["feeds"].append(feed)



    with open(f"{config_folder_path}/{symbol}.config.json", "w") as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    args = load_args()

    symbols_only = args.onlysymbols
    refresh = args.refresh
    input_symbols = args.symbols.replace(" ","").split(",")
    network = args.network
    is_replace = args.replace

    if not os.path.exists(SYMBOLS_PATH) or refresh or symbols_only:
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
            replace_config_file(f"config/{network}", symbol, feeds)
        else:
            update_or_make_config_file(f"config/{network}", symbol, feeds)