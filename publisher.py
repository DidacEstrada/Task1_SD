# EJEMPLO DE PUBLICADOR
import pika

# Conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Exchange de tipo 'fanout' (envía mensajes a todas las colas suscritas (subsribers))
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Ejemplo publicación de mensaje
def publish_message(message):
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print("Enviado %r" % message)
publish_message("Mensaje: Hola mundo!")

connection.close()