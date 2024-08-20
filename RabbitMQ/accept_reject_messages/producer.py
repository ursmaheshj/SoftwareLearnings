import pika

from pika.exchange_type import ExchangeType

connection_parameter = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.exchange_declare(exchange='acceptrejectexchange',exchange_type=ExchangeType.fanout)

message = "Message sent"

while True:
    channel.basic_publish(exchange='acceptrejectexchange',
                        routing_key='test',body=message)
    print(f"Send Message: {message}")
    input('Press any key to continue...')
