import pika
from pika.exchange_type import ExchangeType

def on_message_receive(ch, method, properties, body):
    print(f"Payments Consumer: Message Received: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='mytopicexchange',exchange_type=ExchangeType.topic)

queue = channel.queue_declare(queue='',exclusive=True)

channel.queue_bind(exchange='mytopicexchange',queue=queue.method.queue,routing_key='#.payments')
channel.queue_bind(exchange='mytopicexchange',queue=queue.method.queue,routing_key='all.#')

channel.basic_consume(queue=queue.method.queue,auto_ack=True,
                      on_message_callback=on_message_receive)

print("started consuming")
channel.start_consuming()