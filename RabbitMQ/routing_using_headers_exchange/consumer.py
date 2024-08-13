import pika
from pika.exchange_type import ExchangeType

def on_message_receive(ch, method, properties, body):
    print(f"First Consumer: Message Received: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='headersexchange',exchange_type=ExchangeType.headers)

queue = channel.queue_declare(queue='',exclusive=True)

bind_args = {
    'x-match': 'all',
    'name':'mahesh',
    'age':'53',
}

channel.queue_bind(exchange='headersexchange',queue=queue.method.queue,arguments=bind_args)

channel.basic_consume(queue=queue.method.queue,auto_ack=True,
                      on_message_callback=on_message_receive)

print("started consuming")
channel.start_consuming()