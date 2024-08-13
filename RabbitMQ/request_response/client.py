import pika
import uuid

def on_reply_message_received(ch,method,properties,body):
    print(f'Reply received: {body}')

connection_parameter = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

reply_queue = channel.queue_declare(queue='',exclusive=True)

channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True,
                      on_message_callback=on_reply_message_received)

channel.queue_declare(queue='request-queue')

message = "Requesting a reply from server"

corr_id = str(uuid.uuid4())

print(f'Publishing message:[{corr_id}]')
channel.basic_publish(exchange='',routing_key='request-queue',body=message,
                      properties=pika.BasicProperties(
                          reply_to=reply_queue.method.queue,
                          correlation_id=corr_id,
                      ))

print('starting client')
print(f"Send Message: {message}")
channel.start_consuming()
