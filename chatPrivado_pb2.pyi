from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Misatge(_message.Message):
    __slots__ = ("missatge",)
    MISSATGE_FIELD_NUMBER: _ClassVar[int]
    missatge: str
    def __init__(self, missatge: _Optional[str] = ...) -> None: ...

class chatEmpty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
