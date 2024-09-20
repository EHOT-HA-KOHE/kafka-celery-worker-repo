import time
from datetime import datetime, timedelta

import requests
import redis

from celery.exceptions import Retry, MaxRetriesExceededError, SoftTimeLimitExceeded

from src.loguru_config import logger
from src.celery_connection import app

# from src.database import PgUtils
# from src.env import DexScreenerEnv

# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)


@app.task
def save_new_token(address: str, dex_name: str, network: str, created_at: str):
    # Тут должна быть логика добавления нового токена в БД и редис кеш без инфы вообще только адрес декс сеть и возраст

    # Подключаемся к Redis
    # client = redis.StrictRedis(host="localhost", port=6379, db=0)
    # Пример использования
    # client.set("key", "value")
    # logger.info(client.get("key"))  # Должно вывести 'value' 

    logger.info(f"LOOOOOOL 555 {address = }, {dex_name = }, {network = }, {created_at = }")


@app.task
def update_recent_tokens(self, batch_size=300) -> bool:
    # В будущем подумать над тем чтобы разделить логику и задачи обновления токенов из кеша и те что уже вышли из кеша
    # (те что нет на главной странице их можно обновлять чаще)

    # Функция которая перебирает всю базу данных

    # Получаем токены, младше 24 часов
    cutoff_time = datetime.now() - timedelta(hours=24)
    recent_tokens = Token.objects.filter(created_at__gte=cutoff_time)

    # Разбиваем токены на пакеты по 300 штук
    token_ids = recent_tokens.values_list("id", flat=True)

    for i in range(0, len(token_ids), batch_size):
        batch = token_ids[i : i + batch_size]
        update_tokens_info.delay(batch)


@app.task
def update_tokens_info(
    address: str, delay: int, dex_name: str, network: str
) -> str | None:
    # Сделать чтобы после получения инфы о пачке токенов брался кеш редиса в переменную
    # и когда будет происходить запись в дб циклом проверять если адрес есть в кеше редиса
    # и если да то обновляем данные в кеше редиса

    # dexscreener_url = DexScreenerEnv().connect_str

    # Получаем данные из внешнего API для пакета токенов
    response = requests.post("http://api-proxy/update", json={"token_ids": token_ids})
    data = response.json()

    # Обновляем данные в базе данных
    for token_id, price in data.items():
        token = Token.objects.get(id=token_id)
        token.price = price
        token.save()

    # try:
    #     url = f'{dexscreener_url}/get_token_info/?token_address={address}'
    #     response = requests.get(url)

    #     if response.status_code != 200:
    #         raise Exception(f"Response status code is not 200. Code: {response.status_code}")

    #     response_json_data = response.json()[address]
    #     if response_json_data['status_code'] != 200:
    #         raise Exception(f"Response status code in response is not 200. Code: {response_json_data['status_code']}")

    #     if pairs_info := response_json_data['response_data']['pairs']:
    #         for pair in pairs_info:
    #             if pair['dexId'] == "raydium" and pair['quoteToken']['address'] == SOL_MINT:
    #                 logger.info(f'write to db token_price in {delay} delay')

    #                 with PgUtils() as db:
    #                     token_from_db = db.get_token_by_address(address)

    #                     if not token_from_db['portal_url']:
    #                         portal_url = get_portal_url_from_pair_info(pair)
    #                         if portal_url:
    #                             db.update_token_portal_url(
    #                                 token_from_db['address'],
    #                                 get_portal_url_from_pair_info(pair),
    #                             )

    #                     db.store_token_price(
    #                         token_from_db['id'],
    #                         pair['priceNative'],
    #                         pair['liquidity']['quote'],
    #                         delay,
    #                         dex_name
    #                     )

    #                 return f"End of tracking prices for {address} in {delay} sec delay after start"
    #     else:
    #         logger.error("The address whose information has already been obtained from Dexscreener "
    #                      "does not now exist on Dexscreener now")

    # except Exception as err:
    #     logger.error(f'dont write to db token_price in {delay} delay')
    #     logger.error(err)
