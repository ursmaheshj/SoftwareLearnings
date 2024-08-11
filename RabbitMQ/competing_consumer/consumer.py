import pika
import time
import random

def on_message_receive(ch, method, properties, body):
    process_time = random.randint(1,6)
    print(f"Message Received: {body}. It will take {process_time} to process.")
    time.sleep(process_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)    #Acknowledges that message is received
    print("Finished Processing")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='letterbox')

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='letterbox',on_message_callback=on_message_receive)


print("start consuming")
channel.start_consuming()