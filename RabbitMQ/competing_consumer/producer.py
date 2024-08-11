import pika
import random
import time

connection_parameter = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.queue_declare(queue='letterbox')

messageID = 1

while True:
    message = f"Sending Message | messageID: {messageID}"

    channel.basic_publish(exchange='',routing_key='letterbox',body=message)
    print(f"Send Message: {message}")

    time.sleep(random.randint(1,4))
    messageID += 1