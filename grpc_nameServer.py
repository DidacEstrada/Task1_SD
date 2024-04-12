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
        status = False

        # Verificar si el ID ya está en uso
        if self.redis_client.exists(f"client:{client_id}"):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Client ID already exists. Please provide a different one.")
            return nameServer_pb2.Empty()

        # Guardar en Redis
        key = f"client:{client_id}"
        value = f"IP: {ip_address}, Port: {port}, Status: {status}"
        self.redis_client.set(key, value)

        return nameServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def GetAllClientInfo(self, request, context):
        keys = self.redis_client.keys("client:*")
        client_info_list = []
        for key in keys:
            client_id = key.decode("utf-8").split(":")[1]
            client_data = self.redis_client.get(key).decode("utf-8")
            ip, port, status_str = client_data.split(", ")
            status_str_l = status_str.split(": ")[1].lower()
            status = status_str_l == "true"  #si status_str_l es true es printara true sino false
            client_info_list.append(
                nameServer_pb2.ClientInfo(id=client_id, ip=ip.split(": ")[1], port=port.split(": ")[1], status=status)
            )
        return nameServer_pb2.ClientInfoList(clients=client_info_list)

    def GetClientInfoById(self, request, context):
        client_id = request.id
        key = f"client:{client_id}"
        client_data = self.redis_client.get(key)
        if client_data:
            # Imprimir el valor de client_data antes de la división
            print("Client data before split:", client_data)

            # Dividir la cadena y obtener los componentes
            ip, port, status_str = client_data.decode("utf-8").split(", ")
            status_str_l = status_str.split(": ")[1].lower()
            status = status_str_l == "true"  # si status_str_l es true es printara true sino false

            # Imprimir los componentes después de la división
            print("IP:", ip)
            print("Port:", port)
            print("Status:", status)

            # Construir la respuesta con los componentes
            return nameServer_pb2.ClientInfoResponse(ip=ip.split(": ")[1], port=port.split(": ")[1], status=status)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Client ID not found.")
            return nameServer_pb2.Empty()

    def DeleteClientInfo(self, request, context):
        client_id = request.id
        key = f"client:{client_id}"
        if self.redis_client.exists(key):
            self.redis_client.delete(key)
            return nameServer_pb2.Empty()
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return nameServer_pb2.Empty()

    def ChangeStatus(self, request, context):
        client_id = request.id
        new_status = request.status
        key = f"client:{client_id}"
        client_data = self.redis_client.get(key)
        if client_data:
            ip, port, status = client_data.decode("utf-8").split(", ")
            # Actualizar el estado del cliente
            updated_client_data = f"IP: {ip.split(": ")[1]}, Port: {port.split(": ")[1]}, Status: {new_status}"
            self.redis_client.set(key, updated_client_data)
            return nameServer_pb2.Empty()
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Client ID not found.")
            return nameServer_pb2.Empty()



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




