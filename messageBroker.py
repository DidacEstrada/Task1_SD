import pika


class messageBroker:
    def __init__(self, host='localhost', port=5672, username='guest', password='guest'):
        self.credentials = pika.PlainCredentials(username, password)
        self.parameters = pika.ConnectionParameters(host=host, port=port, credentials=self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def get_group_chats(self):
        group_chats = []

        # Exchange de tipo 'topic' para obtener los nombres
        self.channel.exchange_declare(exchange='amq.topic', exchange_type='topic', passive=True)

        method_frame = self.channel.queue_declare(queue='', passive=True)
        queues = method_frame.method.queue

        # Itera sobre las colas y agrega los IDs de los chats grupales a la lista
        for queue in queues:
            if queue.startswith('chat_'):
                group_chats.append(queue.split('_')[1])
        return group_chats

    def create_group_chat(self, chat_id):
        # Implementa este método para crear un nuevo chat grupal en RabbitMQ
        # Debes utilizar la ID proporcionada para crear el nuevo chat
        pass

    def group_chat_exists(self, chat_id):
        return chat_id in self.get_group_chats()
