from confluent_kafka import Consumer
import os


broker = os.getenv('KAFKA_BROKER', 'kafka:9092')

# Конфигурация Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': broker,
    'group.id': 'kafka-celery-worker-consumer',
    'auto.offset.reset': 'earliest',  # Чтобы начинать с самого начала при первом запуске
    'enable.auto.commit': True        # Чтобы автоматически подтверждать обработку сообщений
})

topic = "save-new-pool-to-db"
consumer.subscribe([topic])

# Poll for new messages from Kafka and print them.
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        print(f"Received message: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    print("Interrupted by user")
except Exception as err:
    print(f"Error: {err}")
finally:
    consumer.close()




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
    