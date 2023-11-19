from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SessionStatus(_message.Message):
    __slots__ = ("Time", "Status")
    TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    Time: _duration_pb2.Duration
    Status: str
    def __init__(self, Time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., Status: _Optional[str] = ...) -> None: ...
