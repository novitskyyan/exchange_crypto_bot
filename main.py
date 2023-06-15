from coinAPI import CoinAPI
from database import Database
from random import randint, random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

URL = "https://rest.coinapi.io/v1/exchangerate/"
API_KEY = "B5E79824-2866-4D9F-9BF5-B04D73EC0A3B"
TOKEN = "6207705247:AAEa9PE9ztQ51bvuZPF2H6Jk4KmiNP4A9TU"
db = Database("users.db")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def correct_count(text):
    if text.count(".") == 1:
        text = text.replace(".", "")
        if text.isdigit():
            return True
        else:
            return False
    return False


def check_balance(user_id, count, crypto):
    if crypto == "btc":
        if float(count) <= db.get_btc(user_id):
            return True
        else:
            return False
    elif crypto == "eth":
        if float(count) <= db.get_eth(user_id):
            return True
        else:
            return False



BALANCE_BTN = KeyboardButton("БАЛАНС")
CHANGE_BTN = KeyboardButton("ОБМЕН")
MAIN_KB = ReplyKeyboardMarkup(resize_keyboard=True)
MAIN_KB.add(BALANCE_BTN, CHANGE_BTN)

BTC_BTN = KeyboardButton("BTC")
ETH_BTN = KeyboardButton("ETH")
CRYPTO_KB = ReplyKeyboardMarkup(resize_keyboard=True)
CRYPTO_KB.add(BTC_BTN, ETH_BTN)

RUB_BTN = KeyboardButton("RUB")
USD_BTN = KeyboardButton("USD")
FIAT_KB = ReplyKeyboardMarkup(resize_keyboard=True)
FIAT_KB.add(RUB_BTN, USD_BTN)

def get_balance(user_id):
    return f"BTC: {db.get_btc(user_id)}\n" \
           f"ETH: {db.get_eth(user_id)}\n" \
           f"RUB: {round(db.get_rub(user_id), 2)}\n" \
           f"USD: {round(db.get_usd(user_id), 2)}"


@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    if db.check_user_by_id(user_id):
        await message.reply("Вы уже имеете кошелёк", reply_markup=MAIN_KB)
    else:
        db.add_user(user_id, "start", random(), random(), randint(1, 100), randint(1, 100))
        db.add_user_to_user_change(user_id)
        await message.reply("Приветствуем Вас в нашем обменнике\n"
                        "Здесь Вы можете менять криптовалюту в фиат", reply_markup=MAIN_KB)


@dp.message_handler()
async def info(message: types.Message):
    user_id = message.from_user.id

    if message.text == "БАЛАНС":
        await message.reply(f"Баланс:\n{get_balance(user_id)}")
    elif message.text == "ОБМЕН" and db.get_state(user_id) == "start":
        db.set_state(user_id, state="crypto")
        await message.reply("Выберите криптовалюту для обмена:", reply_markup=CRYPTO_KB)
    elif message.text == "BTC" and db.get_state(user_id) == "crypto":
        db.set_state(user_id, state="fiat")
        db.set_crypto(user_id, "btc")
        await message.reply("Выберите фиат для перевода: ", reply_markup=FIAT_KB)
    elif message.text == "ETH" and db.get_state(user_id) == "crypto":
        db.set_state(user_id, state="fiat")
        db.set_crypto(user_id, "eth")
        await message.reply("Выберите фиат для перевода: ", reply_markup=FIAT_KB)
    elif message.text == "RUB" and db.get_state(user_id) == "fiat":
        db.set_state(user_id, state="count")
        db.set_fiat(user_id, "rub")
        await message.reply("Выберите количество криптовалюты: ", reply_markup=ReplyKeyboardRemove())
    elif message.text == "USD" and db.get_state(user_id) == "fiat":
        db.set_state(user_id, state="count")
        db.set_fiat(user_id, "usd")
        await message.reply("Выберите количество криптовалюты: ", reply_markup=ReplyKeyboardRemove())
    elif db.get_state(user_id) == "count":
        amount_of_crypto_of_user = message.text
        if correct_count(amount_of_crypto_of_user) and check_balance(user_id, amount_of_crypto_of_user, db.get_crypto(user_id)):
            db.set_count(user_id, float(amount_of_crypto_of_user))
            db.set_state(user_id, "start")
            if db.get_crypto(user_id) == "btc" and db.get_fiat(user_id) == "rub":
                db.set_btc(user_id, db.get_btc(user_id) - float(amount_of_crypto_of_user))
                cA = CoinAPI(URL, API_KEY, "BTC", "RUB")  # url, api_key, token_from, token_to
                add_rub = cA.get_dict_response()["rate"]
                db.set_rub(user_id, db.get_rub(user_id) + add_rub)
            elif db.get_crypto(user_id) == "btc" and db.get_fiat(user_id) == "usd":
                db.set_btc(user_id, db.get_btc(user_id) - float(amount_of_crypto_of_user))
                cA = CoinAPI(URL, API_KEY, "BTC", "USD")  # url, api_key, token_from, token_to
                add_usd = cA.get_dict_response()["rate"]
                db.set_usd(user_id, db.get_usd(user_id) + add_usd)
            elif db.get_crypto(user_id) == "eth" and db.get_fiat(user_id) == "usd":
                db.set_eth(user_id, db.get_eth(user_id) - float(amount_of_crypto_of_user))
                cA = CoinAPI(URL, API_KEY, "ETH", "USD")  # url, api_key, token_from, token_to
                add_usd = cA.get_dict_response()["rate"]
                db.set_usd(user_id, db.get_usd(user_id) + add_usd)
            elif db.get_crypto(user_id) == "eth" and db.get_fiat(user_id) == "rub":
                db.set_eth(user_id, db.get_eth(user_id) - float(amount_of_crypto_of_user))
                cA = CoinAPI(URL, API_KEY, "ETH", "RUB")  # url, api_key, token_from, token_to
                add_rub = cA.get_dict_response()["rate"]
                db.set_rub(user_id, db.get_rub(user_id) + add_rub)
            await message.reply("Перевод успешно выполнен!", reply_markup=MAIN_KB)
        else:
            await message.reply(("Ошибка!"))




executor.start_polling(dp)

#wd = CoinAPI(URL, API_KEY, TOKEN_FROM, TOKEN_TO)

#print(wd.get_dict_response()["rate"])



