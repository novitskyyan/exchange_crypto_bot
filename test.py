from coinAPI import CoinAPI

URL = "https://rest.coinapi.io/v1/exchangerate/"
API_KEY = "B5E79824-2866-4D9F-9BF5-B04D73EC0A3B"

cA = CoinAPI(URL, API_KEY, "BTC", "RUB")  # url, api_key, token_from, token_to
add_rub = cA.get_dict_response()["rate"]
print(add_rub)