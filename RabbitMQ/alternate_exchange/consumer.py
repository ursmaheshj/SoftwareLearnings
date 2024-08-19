import pika
from pika.exchange_type import ExchangeType

def on_message_receive_alt_queue(ch, method, properties, body):
    print(f"Alternate Exchange: Message Received: {body}")
def on_message_receive_main_queue(ch, method, properties, body):
    print(f"Main Exchange: Message Received: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='altexchange',exchange_type=ExchangeType.fanout)
channel.exchange_declare(exchange='mainexchange',exchange_type=ExchangeType.direct,
                         arguments={'alternate-exchange':'altexchange'})

channel.queue_declare(queue='altexchangequeue')
channel.queue_bind(exchange='altexchange',queue='altexchangequeue')
channel.basic_consume(queue='altexchangequeue',auto_ack=True,
                      on_message_callback=on_message_receive_alt_queue)

channel.queue_declare(queue='mainexchangequeue')
channel.queue_bind(exchange='mainexchange',queue='mainexchangequeue',routing_key='test')
channel.basic_consume(queue='mainexchangequeue',auto_ack=True,
                      on_message_callback=on_message_receive_main_queue)

print("started consuming")
channel.start_consuming()