import grpc
import nameServer_pb2
import nameServer_pb2_grpc


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


def switch(argument):
    switch_cases = {
        1: run_subscribe,
        2: run_get_all_clients
    }
    switch_cases.get(argument, run_get_all_clients)()


def run_subscribe():
    channel = grpc.insecure_channel('localhost:50051')
    stub = nameServer_pb2_grpc.NameServerStub(channel)
    while True:
        client_id = input("Enter client ID: ")
        ip = input("Enter IP address: ")
        port = input("Enter port: ")
        if subscribe(stub, client_id, ip, port):
            break


def run_get_all_clients():
    channel = grpc.insecure_channel('localhost:50051')
    stub = nameServer_pb2_grpc.NameServerStub(channel)
    get_all_clients(stub)


def run():

    print("Bienvenido elige una opcion: 1. Subscribirte, 2. Get all clients")
    opcion = int(input("Elige una opcion: "))
    switch(opcion)


if __name__ == '__main__':
    run()
