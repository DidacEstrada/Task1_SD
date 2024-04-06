import asyncio
from concurrent.futures import ThreadPoolExecutor

import grpc
from _socket import gethostname, gethostbyname

import chatPrivado_pb2
import chatPrivado_pb2_grpc
import nameServer_pb2
import nameServer_pb2_grpc


class ChatServicer(chatPrivado_pb2_grpc.ChatServicer):
    def __init__(self):
        self.messages = []

    def EnviarMissatge(self, request, context):
        received_message = request.missatge
        self.messages.append(received_message)
        return chatPrivado_pb2.MisatgeRebut(missatge=f"Missatge rebut: {received_message}")

    def RebreMissatge(self, request, context):
        for message in self.messages:
            yield chatPrivado_pb2.MisatgeRebut(missatge=message)

def serve(ip, port):
    server = grpc.aio.server(ThreadPoolExecutor())
    chatPrivado_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f'{ip}:{port}')
    server.start()
    server.wait_for_termination()

def subscribe(stub, client_id, ip, port):
    try:
        response = stub.AddClientInfo(nameServer_pb2.ClientInfo(id=client_id, ip=ip, port=port))
        print("Client added successfully")
        return True
    except grpc.RpcError as e:
        print("Error:", e.details())  # Mostrar el mensaje de error
        return False


def get_all_clients(stub):
    response = stub.GetAllClientInfo(nameServer_pb2.Empty())
    for client in response.clients:
        print(f"Client ID: {client.id}, IP: {client.ip}, Port: {client.port}")


def get_client_info_by_id(stub, client_id):
    try:
        response = stub.GetClientInfoById(nameServer_pb2.ClientId(id=client_id))
        print(f"Client ID: {client_id}, IP: {response.ip}, Port: {response.port}")
        return response
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print("Client ID not found.")
        else:
            print("Error:", e.details())


def delete_user(client_id):
    channel = grpc.insecure_channel('localhost:50051')
    stub = nameServer_pb2_grpc.NameServerStub(channel)
    try:
        stub.DeleteClientInfo(nameServer_pb2.ClientId(id=client_id))
        print(f"User with ID {client_id} deleted successfully.")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print("User not found.")
        else:
            print("Error:", e.details())


def run_subscribe():
    channel = grpc.insecure_channel('localhost:50051')
    stub = nameServer_pb2_grpc.NameServerStub(channel)
    while True:
        client_id = input("Enter client ID: ")
        ip = get_ip()
        port = input("Enter port: ")
        if subscribe(stub, client_id, ip, port):
            break
    return client_id, ip, port




def get_ip():
    host_name = gethostname()
    ip = gethostbyname(host_name)
    return ip

def run_get_all_clients():
    channel = grpc.insecure_channel('localhost:50051')
    stub = nameServer_pb2_grpc.NameServerStub(channel)
    get_all_clients(stub)


def ConnectChat():
    channel = grpc.insecure_channel('localhost:50051')
    stub = nameServer_pb2_grpc.NameServerStub(channel)
    while True:
        id_amic = input("Dime un id: ")
        response = get_client_info_by_id(stub, id_amic)
        if response:
            ip_amic = response.ip
            port_amic = response.port

            chat_channel = grpc.insecure_channel(f"{ip_amic}:{port_amic}")
            chat_stub = chatPrivado_pb2_grpc.ChatStub(chat_channel)

            async def send_message():
                while True:
                    mensaje = input("Tú: ")
                    respuesta = await chat_stub.EnviarMissatge(chatPrivado_pb2.MisatgeEnviat(missatge=mensaje))
                    print(f"{id_amic}: {respuesta.missatge}")

            async def receive_messages():
                async for mensaje_entrante in chat_stub.RebreMissatge(chatPrivado_pb2.chatEmpty()):
                    print(f"{id_amic}: {mensaje_entrante.missatge}")

                await asyncio.gather(send_message(), receive_messages())
            break
        else:
            print("El cliente con el ID proporcionado no está disponible.")
            opcion = input("¿Quieres intentar con otro ID? (y/n): ")
            if opcion.lower() != 'y':
                break

def run():
    mi_id, ip, port = run_subscribe()
    serve(ip, port)
    while True:
            print("Bienvenido elige una opcion: 1. Connect chat, 2. Subscribe to group chat, 3. Discover chats, "
                  "4. Acces to insult server, 0. Exit")
            opcion = int(input("Elige una opcion: "))
            if opcion == 1:
                ConnectChat()
            elif opcion == 2:
                run_get_all_clients()
            elif opcion == 3:
                run_get_all_clients()
            elif opcion == 0:
                delete_user(mi_id)
                print("Saliendo...")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")


if __name__ == '__main__':
    run()
