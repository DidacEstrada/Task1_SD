import pika
import requests
import json
import time


class RabbitMQServer:
    def __init__(self, host='localhost', port=5672, management_port=15672, username='guest', password='guest'):
        self.host = host
        self.port = port
        self.management_port = management_port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
    def sub_insulting_server(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    def create_exchange(self, exchange_name, exchange_type='direct'):
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    def create_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name)

    def bind_queue_to_exchange(self, queue_name, exchange_name, routing_key):
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    def subscribe_to_queue(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    def start_consuming(self):
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()

    def get_all_queues(self):
        url = f'http://{self.host}:{self.management_port}/api/queues'
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            queues = [queue['name'] for queue in response.json()]
            return queues
        else:
            print("Failed to fetch queues:", response.text)
            return []

    def subscribe_group_chat(self, queue_name, callback):
        all_queues = self.get_all_queues_exchange("chat_group_exchange")
        if queue_name in all_queues:
            self.subscribe_to_queue(queue_name, callback)

        else:
            self.channel.queue_declare(queue=queue_name)
            self.channel.queue_bind(exchange="chat_group_exchange", queue=queue_name, routing_key=queue_name + '_key')
            time.sleep(1)
            self.subscribe_to_queue(queue_name, callback)

    def publish_message(self, exchange_name, routing_key, message):
        self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)

    def publish_discovery_event(self):
        self.channel.basic_publish(exchange="chat_discovery_exchange", routing_key='event_discovery_key',
                                   body="Quien esta conectado?")

    def get_all_queues_exchange(self, exchange_name):
        url = f"http://{self.host}:{self.management_port}/api/exchanges/%2f/{exchange_name}/bindings/source"
        try:
            response = requests.get(url, auth=(self.username, self.password))
            response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
            queues = [binding['destination'] for binding in response.json()]
            return queues
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener las colas de la exchange {exchange_name}: {e}")
            return []

    def unsubscribe_from_queue(self, queue_name):
        self.channel.basic_cancel(queue_name)
        print(f"Desuscripción de la cola '{queue_name}' realizada.")

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def subscribe_to_discovery_events(self, callback):
        self.channel.basic_consume(queue="event_discovery", on_message_callback=callback, auto_ack=True)

    def discover_chats(self, callback):
        self.channel.basic_consume(queue="chat_discovery", on_message_callback=callback, auto_ack=True)
        group_chats = self.get_all_queues_exchange("chat_group_exchange")
        message_body = json.dumps(group_chats).encode('utf-8')
        self.publish_message("chat_discovery_exchange", "chat_discovery_key", message_body)


# Uso del método get_all_queues
if __name__ == "__main__":
    server = RabbitMQServer()
    server.connect()
    #server.create_exchange("chat_group_exchange", "direct")
    #server.create_exchange("chat_discovery_exchange", "direct")
    #server.create_queue("chat_discovery")
    #server.bind_queue_to_exchange("chat_discovery", "chat_discovery_exchange", "chat_discovery_key")
    #server.create_queue("event_discovery")
    #server.bind_queue_to_exchange("event_discovery", "chat_discovery_exchange", "event_discovery_key")
    queues = server.get_all_queues_exchange("chat_discovery_exchange")
    print("All queues:", queues)
    server.close_connection()
