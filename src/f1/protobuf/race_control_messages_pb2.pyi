from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RaceControlMessages(_message.Message):
    __slots__ = ("Time", "Category", "Message", "Status", "Flag", "Scope", "Sector", "RacingNumber")
    TIME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FLAG_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    SECTOR_FIELD_NUMBER: _ClassVar[int]
    RACINGNUMBER_FIELD_NUMBER: _ClassVar[int]
    Time: _timestamp_pb2.Timestamp
    Category: str
    Message: str
    Status: str
    Flag: str
    Scope: str
    Sector: float
    RacingNumber: str
    def __init__(self, Time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., Category: _Optional[str] = ..., Message: _Optional[str] = ..., Status: _Optional[str] = ..., Flag: _Optional[str] = ..., Scope: _Optional[str] = ..., Sector: _Optional[float] = ..., RacingNumber: _Optional[str] = ...) -> None: ...
