import pika
from pika.exchange_type import ExchangeType

def on_message_receive1(ch, method, properties, body):
    print(f"First Queue: Message Received: {body}")

def on_message_receive2(ch, method, properties, body):
    print(f"Second Queue: Message Received: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='hashingexchange',exchange_type='x-consistent-hash')

channel.queue_declare(queue='queue1')
channel.queue_bind(exchange='hashingexchange',queue='queue1',routing_key='1')
channel.basic_consume(queue='queue1',auto_ack=True,
                      on_message_callback=on_message_receive1)

channel.queue_declare(queue='queue2')
channel.queue_bind(exchange='hashingexchange',queue='queue2',routing_key='4')
channel.basic_consume(queue='queue2',auto_ack=True,
                      on_message_callback=on_message_receive2)

print("started consuming")
channel.start_consuming()