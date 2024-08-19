import pika
from random import randint

from pika.exchange_type import ExchangeType

connection_parameter = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.exchange_declare(exchange='hashingexchange',exchange_type='x-consistent-hash')

routing_key = str(randint(100,999))

message = "This messages is hashed"

channel.basic_publish(exchange='hashingexchange',routing_key=routing_key,body=message)

print(f"Send Message: {message}")

connection.close()