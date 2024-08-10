import pika

connection_parameter = pika.ConnectionParameters('http://localhost:5672/')

connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()

channel.queue_declare(queue='letterbox')

message = "Hello this is mahesh"

channel.basic_publish(exchange='',routing_key='letterbox',body=message)

print(f"Send Message: {message}")

connection.close()