from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientInfo(_message.Message):
    __slots__ = ("id", "ip", "port", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    ip: str
    port: str
    status: bool
    def __init__(self, id: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[str] = ..., status: bool = ...) -> None: ...

class ClientId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ClientStatus(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: bool
    def __init__(self, id: _Optional[str] = ..., status: bool = ...) -> None: ...

class ClientInfoResponse(_message.Message):
    __slots__ = ("ip", "port", "status")
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ip: str
    port: str
    status: bool
    def __init__(self, ip: _Optional[str] = ..., port: _Optional[str] = ..., status: bool = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClientInfoList(_message.Message):
    __slots__ = ("clients",)
    CLIENTS_FIELD_NUMBER: _ClassVar[int]
    clients: _containers.RepeatedCompositeFieldContainer[ClientInfo]
    def __init__(self, clients: _Optional[_Iterable[_Union[ClientInfo, _Mapping]]] = ...) -> None: ...
