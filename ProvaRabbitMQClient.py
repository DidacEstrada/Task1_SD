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

    def publish_message(self, exchange_name, routing_key, message):
        self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
        print(f"Mensaje enviado: '{message}'")

    def close_connection(self):
        if self.connection:
            self.connection.close()

# Ejemplo de uso
if __name__ == "__main__":
    client = RabbitMQClient()
    client.connect()
    exchange_name = 'chat_group_exchange'  # Nombre de la exchange
    routing_key = 'prova1_key'  # Clave de enrutamiento
    message = 'Hola, Primer Suscriptor!'  # Mensaje a enviar
    client.publish_message(exchange_name, routing_key, message)
    client.close_connection()