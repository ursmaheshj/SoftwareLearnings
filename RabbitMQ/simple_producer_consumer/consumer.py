import pika

def on_message_receive(ch, method, properties, body):
    print(f"New Message Received: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='letterbox')

channel.basic_consume(queue='letterbox',auto_ack=True,
                      on_message_callback=on_message_receive)


print("start consuming")
channel.start_consuming()