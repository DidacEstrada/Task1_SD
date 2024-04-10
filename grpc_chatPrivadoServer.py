import grpc
from concurrent import futures
import time

import chatPrivado_pb2
import chatPrivado_pb2_grpc

from chatPrivadoService import chatPrivadoService


class ChatPrivadoServiceServicer(chatPrivado_pb2_grpc.ChatServicer):
    def EnviarMisatge(self, request, context):
        chatPrivadoService.enviarmisatge(request)
        response = chatPrivado_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


def serve():
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # use the generated function `add_InsultingServiceServicer_to_server`
    # to add the defined class to the server
    chatPrivado_pb2_grpc.add_ChatServicer_to_server(
        ChatPrivadoServiceServicer(), server)

    # listen on port 50052
    print('Starting server. Listening on port 50052.')
    server.add_insecure_port('0.0.0.0:50053')
    server.start()

    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        while True:
            time.sleep(400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
