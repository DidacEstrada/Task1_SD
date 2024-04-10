import grpc

import chatPrivado_pb2_grpc
import chatPrivado_pb2

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50052')

# create a stub (client)
stub = chatPrivado_pb2_grpc.ChatStub(channel)

# create a valid request message
misatge = chatPrivado_pb2.Misatge(misatge='Hola')
stub.EnviarMisatge(misatge)
