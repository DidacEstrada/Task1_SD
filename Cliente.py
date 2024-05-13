import json
import time
import threading

import grpc
from _socket import gethostname, gethostbyname
from functools import partial
from RabbitMQServer import RabbitMQServer

import chatPrivado_pb2
import chatPrivado_pb2_grpc
import nameServer_pb2
import nameServer_pb2_grpc
import grpc_chatPrivadoServer


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
        print(f"Client ID: {client.id}, IP: {client.ip}, Port: {client.port}, Status: {client.status}")


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


def ConnectChat(ip_amic, port_amic, status_amic, mi_id):
    if status_amic == True:
        try:
            # Intentar conectarse a los servidores gRPC
            channel2 = grpc.insecure_channel(f'localhost:{port_amic}')
            chat_stub = chatPrivado_pb2_grpc.ChatStub(channel2)
            print("Chat Iniciado")
            chat = True
            while chat:
                mensaje = input()
                chat_stub.EnviarMisatge(chatPrivado_pb2.Misatge(id=mi_id, misatge=mensaje))
                print("Mensaje enviado")
                if mensaje == "Adeu":
                    chat = False

        except grpc.aio.AioRpcError as e:
            # Capturar errores de conexión
            print("Error al conectar con el servidor gRPC:", e)
    else:
        print("No esta conectat")


def test():
    # open a gRPC channel
    channel = grpc.insecure_channel('localhost:50052')
    # create a stub (client)
    stub = chatPrivado_pb2_grpc.ChatStub(channel)
    # create a valid request message
    misatge = chatPrivado_pb2.Misatge(misatge='Hola')
    stub.EnviarMisatge(misatge)


def canviarStatus(client_id, new_status):
    channel = grpc.insecure_channel('localhost:50051')
    # create a stub (client)
    stub = nameServer_pb2_grpc.NameServerStub(channel)
    request = stub.ChangeStatus(nameServer_pb2.ClientStatus(id=client_id, status=new_status))


def SaberDadesAmic():
    channel = grpc.insecure_channel('localhost:50051')
    stub = nameServer_pb2_grpc.NameServerStub(channel)
    while True:
        id_amic = input("Dime un id: ")
        response = get_client_info_by_id(stub, id_amic)
        if response:
            ip_amic = response.ip
            port_amic = response.port
            status_amic = response.status
            return ip_amic, port_amic, status_amic

        else:
            print("El cliente con el ID proporcionado no está disponible.")
            opcion = input("¿Quieres volver a intentar connectarte? (y/n): ")
            if opcion.lower() != 'y':
                ip_amic = ""
                port_amic = "n"  # Controlar decisions
                return ip_amic, port_amic


def callback(ch, method, properties, body):
    print("Mensaje recibido:", body.decode('utf-8'))


def callback_insult(ch, method, properties, body):
    print("Insulto recibido:", body.decode('utf-8'))

def callback_chats(ch, method, properties, body):
    print(body.decode('utf-8'))


def callback_discovery(ch, method, properties, body, server, mi_id, ip, port):
    message = body.decode('utf-8').split(',')

    # Extraer el ID del primer elemento
    id_received = message[0]
    response = {
        "id": mi_id,
        "ip": ip,
        "port": port,
    }

    message_body = json.dumps(response).encode('utf-8')
    server.publish_message("chat_discovery_exchange", id_received + '_discovery_key', message_body)


def chat_grupal(server, grup_id):
    chat = True
    while chat:
        mensaje = input("-> ")
        server.publish_message_fanout(grup_id, mensaje)
        print("Mensaje enviado")
        if mensaje == "Adeu":
            chat = False


def run():
    mi_id, ip, port = run_subscribe()
    threading.Thread(target=grpc_chatPrivadoServer.serve, args=(port,)).start()
    server = RabbitMQServer()
    server.connect()
    tag_event = server.subscribe_to_discovery_events(partial(callback_discovery, server=server, mi_id=mi_id, ip=ip, port=port), mi_id)
    time.sleep(0.5)
    server.subscribe_to_queue("insulting_server", callback_insult)
    time.sleep(0.5)
    threading.Thread(target=server.start_consuming).start()
    time.sleep(0.5)
    while True:
        print("Bienvenido elige una opcion: 1. Connect chat, 2. Subscribe to group chat, 3. Discover chats, "
              "4. Acces to insult server, 0. Exit")
        opcion = int(input("Elige una opcion: "))
        if opcion == 1:
            canviarStatus(mi_id, True)
            ip_amic, port_amic, status_amic = SaberDadesAmic()
            if port_amic != "n":
                ConnectChat(ip_amic, port_amic, status_amic, mi_id)
            canviarStatus(mi_id, False)
        elif opcion == 2:
            grup_id = input("Dime el nombre del grupo: ")
            tag_chat = server.subscribe_group_chat(grup_id, mi_id, callback)
            time.sleep(2)
            print("Bienvenido al grupo, para salir escribe 'Adeu' ")
            chat_grupal(server, grup_id)
            time.sleep(1)
            server.unsubscribe_from_queue(tag_chat)

        elif opcion == 3:
            print("Buscando chats...")
            tag_discovery = server.subscribe_to_chat_discovery(callback_chats, mi_id)
            time.sleep(2)
            server.publish_discovery_event(mi_id)
            print("Todos los chats:")
            time.sleep(2)
            server.unsubscribe_from_queue(tag_discovery)

        elif opcion == 4:
            insult = input("Escribe tu insulto: ")
            server.send_insult(insult)
            time.sleep(1)

        elif opcion == 0:
            delete_user(mi_id)
            server.unsubscribe_from_queue(tag_event)
            server.stop_consuming()
            server.close_connection()
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")


if __name__ == '__main__':
    run()
