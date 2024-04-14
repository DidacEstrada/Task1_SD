# EJEMPLO DE SUBSCRIPTOR
import pika

# Recibir mensajes
def callback(ch, method, properties, body):
    print("Recibido: %r" % body.decode('utf-8'))

# Conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Exchange de tipo 'fanout' (envía mensajes a todas las colas suscritas)
channel.exchange_declare(exchange='logs', exchange_type='fanout')


result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue


channel.queue_bind(exchange='logs', queue=queue_name)

print('Esperando mensajes...')

# Callback para manejar los mensajes entrantes
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()