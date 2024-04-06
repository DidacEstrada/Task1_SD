# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chatPrivado_pb2 as chatPrivado__pb2


class ChatStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.EnviarMissatge = channel.unary_unary(
                '/Chat/EnviarMissatge',
                request_serializer=chatPrivado__pb2.Misatge.SerializeToString,
                response_deserializer=chatPrivado__pb2.Misatge.FromString,
                )


class ChatServicer(object):
    """Missing associated documentation comment in .proto file."""

    def EnviarMissatge(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'EnviarMissatge': grpc.unary_unary_rpc_method_handler(
                    servicer.EnviarMissatge,
                    request_deserializer=chatPrivado__pb2.Misatge.FromString,
                    response_serializer=chatPrivado__pb2.Misatge.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Chat', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Chat(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def EnviarMissatge(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chat/EnviarMissatge',
            chatPrivado__pb2.Misatge.SerializeToString,
            chatPrivado__pb2.Misatge.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
