import pika
from pika.exchange_type import ExchangeType

def on_message_receive_dl_queue(ch, method, properties, body):
    print(f"Dead Letter Exchange: Message Received: {body}")
def on_message_receive_main_queue(ch, method, properties, body):
    print(f"Main Exchange: Message Received: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='mainexchange',exchange_type=ExchangeType.direct)
channel.exchange_declare(exchange='dlexchange',exchange_type=ExchangeType.fanout)

channel.queue_declare(queue='mainexchangequeue',arguments={
        'x-dead-letter-exchange':'dlexchange','x-message-ttl':1000})
channel.queue_bind(exchange='mainexchange',queue='mainexchangequeue',routing_key='test')
# channel.basic_consume(queue='mainexchangequeue',auto_ack=True,
#                       on_message_callback=on_message_receive_main_queue)

channel.queue_declare(queue='dlexchangequeue')
channel.queue_bind(exchange='dlexchange',queue='dlexchangequeue')
channel.basic_consume(queue='dlexchangequeue',auto_ack=True,
                      on_message_callback=on_message_receive_dl_queue)

print("started consuming")
channel.start_consuming()