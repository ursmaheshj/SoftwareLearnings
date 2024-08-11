import pika
from pika.exchange_type import ExchangeType

connection_parameter = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.exchange_declare(exchange='pubsub',exchange_type=ExchangeType.fanout)

message = "Hello this is a broadcast message"

channel.basic_publish(exchange='pubsub',routing_key='',body=message)

print(f"Send Message: {message}")

connection.close()