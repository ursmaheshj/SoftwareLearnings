import pika
from pika.exchange_type import ExchangeType

connection_parameter = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.exchange_declare(exchange='mytopicexchange',exchange_type=ExchangeType.topic)

message = "Hello this is a routing related message 4"

channel.basic_publish(exchange='mytopicexchange',routing_key='user.europe.payments',body=message)

print(f"Send Message: {message}")

connection.close()