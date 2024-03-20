import grpc
import nameServer_pb2
import nameServer_pb2_grpc

def subscribe(stub, client_id, ip, port):
    response = stub.AddClientInfo(nameServer_pb2.ClientInfo(id=client_id, ip=ip, port=port))
    response2 = stub.GetAllClientInfo
    print(response2)
    print("T'has connectat amb exit")


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = nameServer_pb2_grpc.NameServerStub(channel)
    client_id = input("Enter client ID: ")
    ip = input("Enter IP address: ")
    port = input("Enter port: ")
    subscribe(stub, client_id, ip, port)

if __name__ == '__main__':
    run()