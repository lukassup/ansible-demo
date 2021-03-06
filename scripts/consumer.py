#!/usr/bin/env python
import os
import time

import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/conejo")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "conejo")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "conejo")


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


if __name__ == "__main__":
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            virtual_host=RABBITMQ_VHOST,
            credentials=credentials,
        )
    )
    channel = connection.channel()
    channel.exchange_declare(exchange="test")
    channel.queue_declare(queue="test", arguments={"x-message-ttl": 3600})
    channel.queue_bind(exchange="test", queue="test")
    print(" [*] Waiting for logs. To exit press CTRL+C")
    channel.basic_consume(queue="test", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
