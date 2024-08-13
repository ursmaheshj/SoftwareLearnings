import pika

from pika.exchange_type import ExchangeType

connection_parameter = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.exchange_declare(exchange='firstexchange',exchange_type=ExchangeType.direct)
channel.exchange_declare(exchange='secondexchange',exchange_type=ExchangeType.fanout)

channel.exchange_bind('secondexchange','firstexchange')

message = "This messages goes from multiple exchanges"

channel.basic_publish(exchange='firstexchange',routing_key='',body=message)

print(f"Send Message: {message}")

connection.close()