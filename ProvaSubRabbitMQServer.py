import pika

class RabbitMQClient:
    def __init__(self, host='localhost', port=5672, username='guest', password='guest'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def subscribe_to_queue(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f"Suscripción a la cola '{queue_name}' realizada. Esperando mensajes...")

    def start_consuming(self):
        self.channel.start_consuming()

    def close_connection(self):
        if self.connection:
            self.connection.close()

# Función de devolución de llamada para procesar los mensajes recibidos
def callback(ch, method, properties, body):
    print("Mensaje recibido:", body)

# Ejemplo de uso
if __name__ == "__main__":
    client = RabbitMQClient()
    client.connect()
    queue_name = 'prova1'  # Nombre de la cola a la que suscribirse
    client.subscribe_to_queue(queue_name, callback)
    client.start_consuming()