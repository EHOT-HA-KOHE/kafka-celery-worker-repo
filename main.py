import json
import os
import re
import time

from confluent_kafka import Consumer

from celery_tasks import save_new_token
from src.loguru_config import logger


KAFKA_TOPIC = "save-new-pool-to-db"


broker = os.getenv('KAFKA_BROKER', 'kafka:9092')
consumer = Consumer({
    'bootstrap.servers': broker,
    'group.id': 'kafka-celery-worker-consumer',
    'auto.offset.reset': 'earliest',  # Чтобы начинать с самого начала при первом запуске
    'enable.auto.commit': True        # Чтобы автоматически подтверждать обработку сообщений
})
consumer.subscribe([KAFKA_TOPIC, ])

# Poll for new messages from Kafka and print them.
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logger.error(f"Error: {msg.error()}")
            continue

        message_str = msg.value().decode('utf-8')
        json_str = re.sub(r"(?<!\\)'", '"', message_str)
        data = json.loads(json_str)

        # data = {'address': '0xu785JKGUInouyrou2chgwcjkbwi453bhjv', 'dex_name': 'RADIUM', 'network': 'SOL', 'created_at': '2024-09-19T17:11:40.829346'}

        result = save_new_token.delay(
            address=data.get('address'),
            dex_name=data.get('dex_name'),
            network=data.get('network'),
            created_at=data.get('created_at'),
        )
        print(result.ready())  # Проверка, завершена ли задача
        print(result.result)

except KeyboardInterrupt:
    logger.error("Interrupted by user")
except Exception as err:
    logger.error(f"Error: {err}")
finally:
    logger.error('End of programm 7296')
    consumer.close()
