from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Misatge(_message.Message):
    __slots__ = ("id", "misatge")
    ID_FIELD_NUMBER: _ClassVar[int]
    MISATGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    misatge: str
    def __init__(self, id: _Optional[str] = ..., misatge: _Optional[str] = ...) -> None: ...
