from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientInfo(_message.Message):
    __slots__ = ("id", "ip", "port")
    ID_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    id: str
    ip: str
    port: str
    def __init__(self, id: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClientInfoList(_message.Message):
    __slots__ = ("clients",)
    CLIENTS_FIELD_NUMBER: _ClassVar[int]
    clients: _containers.RepeatedCompositeFieldContainer[ClientInfo]
    def __init__(self, clients: _Optional[_Iterable[_Union[ClientInfo, _Mapping]]] = ...) -> None: ...
