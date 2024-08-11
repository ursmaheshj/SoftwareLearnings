import pika
from pika.exchange_type import ExchangeType

connection_parameter = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.exchange_declare(exchange='routing',exchange_type=ExchangeType.direct)

message = "Hello this is a routing related message"

channel.basic_publish(exchange='routing',routing_key='paymentsonly',body=message)

print(f"Send Message: {message}")

connection.close()