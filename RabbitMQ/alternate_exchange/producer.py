import pika

from pika.exchange_type import ExchangeType

connection_parameter = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.exchange_declare(exchange='altexchange',exchange_type=ExchangeType.fanout)
channel.exchange_declare(exchange='mainexchange',exchange_type=ExchangeType.direct,
                         arguments={'alternate-exchange':'altexchange'})

message = "This messages is to test alternate exchange"

channel.basic_publish(exchange='mainexchange',routing_key='test',body=message)
# channel.basic_publish(exchange='mainexchange',routing_key='adsf',body=message)

print(f"Send Message: {message}")

connection.close()