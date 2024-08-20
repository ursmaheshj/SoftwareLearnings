import pika
from pika.exchange_type import ExchangeType

def on_message_receive(ch, method, properties, body):
    if method.delivery_tag % 5 == 0 :
        ch.basic_ack(delivery_tag=method.delivery_tag,requeue=False,multiple=True)
    print(f"Message Received: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='acceptrejectexchange',exchange_type=ExchangeType.fanout)

channel.queue_declare(queue='letterbox')
channel.queue_bind(exchange='acceptrejectexchange',queue='letterbox')
channel.basic_consume(queue='letterbox',on_message_callback=on_message_receive)

print("started consuming")
channel.start_consuming()