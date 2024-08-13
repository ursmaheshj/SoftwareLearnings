import pika

from pika.exchange_type import ExchangeType

connection_parameter = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.exchange_declare(exchange='headersexchange',exchange_type=ExchangeType.headers)

message = "This messages will be sent with headers"

channel.basic_publish(exchange='headersexchange',routing_key='',body=message,
                      properties=pika.BasicProperties(
                          headers={'name':'mahesh','age':'53'}
                      ))

print(f"Send Message: {message}")

connection.close()