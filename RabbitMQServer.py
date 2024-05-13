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

    def create_exchange(self, exchange_name, exchange_type):
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    def create_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name)

    def bind_queue_to_exchange(self, queue_name, exchange_name):
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name)


    def bind_queue_to_exchange_direct(self, queue_name, exchange_name, key):
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=key)


    def subscribe_to_queue(self, queue_name, callback):
        consumer_tag = self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        return consumer_tag

    def start_consuming(self):
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()

    def send_insult(self, insult):
        self.channel.basic_publish(exchange='', routing_key="insulting_server", body=insult)

    def publish_message(self, exchange_name, routing_key, message):
        self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)

    def exchange_exists(self, exchange_name):
        url = f'http://{self.host}:{self.management_port}/api/exchanges/%2f/{exchange_name}'
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            print(f"Failed to check exchange existence. Status code: {response.status_code}")
            return False

    def queue_exists(self, queue_name):
        url = f'http://{self.host}:{self.management_port}/api/queues/%2f/{queue_name}'
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            print(f"Failed to check queue existence. Status code: {response.status_code}")
            return False

    def subscribe_group_chat(self, exchange_name, mi_id, callback):
        exists = self.exchange_exists(exchange_name)
        if exists:
            self.create_queue(mi_id)
            time.sleep(1)
            self.bind_queue_to_exchange(mi_id, exchange_name)
            time.sleep(1)
            tag = self.subscribe_to_queue(mi_id, callback)
            print("Añadido a grupo")
            return tag
        else:
            self.create_exchange(exchange_name, "fanout")
            time.sleep(1)
            self.create_queue(mi_id)
            time.sleep(1)
            self.bind_queue_to_exchange(mi_id, exchange_name)
            time.sleep(1)
            tag = self.subscribe_to_queue(mi_id, callback)
            print("Grupo creado")
            return tag

    def publish_message_fanout(self, exchange_name, message):
        self.channel.basic_publish(exchange=exchange_name, routing_key='', body=message)

    def publish_discovery_event(self, mi_id):
        message = mi_id + ',Quien esta conectado?'
        self.channel.basic_publish(exchange="discovery_event_exchange", routing_key='',
                                   body=message)

    def unsubscribe_from_queue(self, consumer_tag):
        self.channel.basic_cancel(consumer_tag)
        time.sleep(1)
        print(f"Desuscripción realizada.")

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def subscribe_to_discovery_events(self, callback, mi_id):
        queue = mi_id + '_event'
        exists = self.queue_exists(queue)
        if exists:
            tag = self.subscribe_to_queue(queue, callback)
            return tag
        else:
            self.create_queue(queue)
            time.sleep(1)
            self.bind_queue_to_exchange(queue, "discovery_event_exchange")
            time.sleep(1)
            tag = self.subscribe_to_queue(queue, callback)
            return tag

    def subscribe_to_chat_discovery(self, callback, mi_id):
        queue = mi_id + '_discovery'
        self.create_queue(queue)
        time.sleep(1)
        self.bind_queue_to_exchange_direct(queue, "chat_discovery_exchange", queue + '_key')
        time.sleep(1)
        tag = self.subscribe_to_queue(queue, callback)
        return tag

# Uso del método get_all_queues
if __name__ == "__main__":
    server = RabbitMQServer()
    server.connect()
    server.create_queue("insulting_server")
    server.create_exchange("discovery_event_exchange", "fanout")
    server.create_exchange("chat_discovery_exchange", "direct")
    server.close_connection()
