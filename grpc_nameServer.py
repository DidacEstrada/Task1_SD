import grpc
import redis

from concurrent import futures
import time

# import the generated classes
import nameServer_pb2
import nameServer_pb2_grpc

# create a class to define the server functions, derived from
# nameServer_pb2_grpc.NameServiceServicer
class NameServer(nameServer_pb2_grpc.NameServerServicer):
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0) # conexion redis con su host puerto y la base de datos numero 0 (db=0)


    def AddClientInfo(self, request, context):
        client_id = request.id
        ip_address = request.ip
        port = request.port

        # Verificar si el ID ya está en uso
        if self.redis_client.exists(f"client:{client_id}"):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Client ID already exists. Please provide a different one.")
            return nameServer_pb2.Empty()

        # Guardar en Redis
        key = f"client:{client_id}"
        value = f"IP: {ip_address}, Port: {port}"
        self.redis_client.set(key, value)

        return nameServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def GetAllClientInfo(self, request, context):
        keys = self.redis_client.keys("client:*")
        client_info_list = []
        for key in keys:
            client_id = key.decode("utf-8").split(":")[1]
            client_data = self.redis_client.get(key).decode("utf-8")
            ip, port = client_data.split(", ")
            client_info_list.append(
                nameServer_pb2.ClientInfo(id=client_id, ip=ip.split(": ")[1], port=port.split(": ")[1]))
        return nameServer_pb2.ClientInfoList(clients=client_info_list)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    nameServer_pb2_grpc.add_NameServerServicer_to_server(NameServer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print("Server started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()




