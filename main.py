from confluent_kafka import Consumer
import os

# LOOOOOOOOOOOOOOOL

# broker = os.getenv('KAFKA_BROKER', 'localhost:9092')
broker = '127.0.0.1:9092'

# Конфигурация Kafka Consumer
# producer = Consumer({'bootstrap.servers': broker})

consumer = Consumer({'bootstrap.servers': broker, 'group.id': 'kafka-celery-worker-consumer',})

topic = "save-new-pool-to-db"
consumer.subscribe([topic])

# Poll for new messages from Kafka and print them.
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        # print('LOL')
        print(msg.value().decode('utf-8'))
except Exception as err:
    print(err)

for message in consumer.consume():
    print(f"Consumer received message: {message.value.decode()}")



# class TokenPriceCollector:
#     def __init__(self):
#         self.intervals = [1, 2, 5, 10, 15, 30, 45, 60, 90, 180, 360, 720, 1440]

#     async def listen_new_tokens(self):
#         raise NotImplementedError

#     def wait_token_on_dexscreener_and_track_price(self, address: str, dex_name: str, network: str) -> bool:
#         # print(f'{address = }, {dex_name = }, {network = }')
#         try:
#             res = wait_token_on_dexscreener.delay(address, dex_name, network)
#             is_success = res.get()
#         except TimeLimitExceeded as err:
#             logger.error(f"TimeLimitExceeded: {err}")
#             is_success = False
#         except TimeoutError as err:
#             logger.error(f"TimeoutError: {err}")
#             is_success = False

#         if is_success:
#             logger.info(f'write to db token_price in 0 delay')
#             for interval in self.intervals:
#                 interval *= 60
#                 track_price.apply_async((address, interval, dex_name, network,), countdown=interval)
#             return True
#         return False
    