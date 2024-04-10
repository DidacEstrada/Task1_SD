import asyncio
from concurrent import futures
import time
import threading

import grpc
from _socket import gethostname, gethostbyname

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


def ConnectChat(ip_amic, port_amic, port):
    try:
        # Intentar conectarse a los servidores gRPC
        channel2 = grpc.insecure_channel(f'localhost:{port_amic}')
        chat_stub = chatPrivado_pb2_grpc.ChatStub(channel2)
        while True:
            print("Conexión exitosa con el servidor gRPC.")
            mensaje = input("Tú: ")
            chat_stub.EnviarMissatge(chatPrivado_pb2.Misatge(missatge=mensaje))
            print("Mensaje enviado")
            # mensajes_recibidos = mi_chat_stub.RecibirMensajes(request)
            # for misatge in mensajes_recibidos.misatges:
            #    print(f"{misatge}")

    except grpc.aio.AioRpcError as e:
        # Capturar errores de conexión
        print("Error al conectar con el servidor gRPC:", e)


def test():
    # open a gRPC channel
    channel = grpc.insecure_channel('localhost:50052')

    # create a stub (client)
    stub = chatPrivado_pb2_grpc.ChatStub(channel)

    # create a valid request message
    misatge = chatPrivado_pb2.Misatge(misatge='Hola')
    stub.EnviarMisatge(misatge)


def canviarStatus():
    channel = grpc.insecure_channel('localhost:50052')
    # create a stub (client)
    stub = chatPrivado_pb2_grpc.ChatStub(channel)
    misatge =





def SaberDadesAmic():
    channel = grpc.insecure_channel('localhost:50051')
    stub = nameServer_pb2_grpc.NameServerStub(channel)
    while True:
        id_amic = input("Dime un id: ")
        response = get_client_info_by_id(stub, id_amic)
        if response:
            ip_amic = response.ip
            port_amic = response.port
            return ip_amic, port_amic

        else:
            print("El cliente con el ID proporcionado no está disponible.")
            opcion = input("¿Quieres volver a intentar connectarte? (y/n): ")
            if opcion.lower() != 'y':
                ip_amic = ""
                port_amic = "n"  # Controlar decisions
                return ip_amic, port_amic


def run():
    mi_id, ip, port = run_subscribe()
    threading.Thread(target=grpc_chatPrivadoServer.serve).start()
    time.sleep(0.5)
    while True:
        print("Bienvenido elige una opcion: 1. Connect chat, 2. Subscribe to group chat, 3. Discover chats, "
              "4. Acces to insult server, 0. Exit")
        opcion = int(input("Elige una opcion: "))
        if opcion == 1:
            ip_amic, port_amic = SaberDadesAmic()
            if port_amic != "n":
                test()
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
