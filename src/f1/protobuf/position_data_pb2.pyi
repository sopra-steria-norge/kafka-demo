from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PositionData(_message.Message):
    __slots__ = ("Date", "Status", "X", "Y", "Z", "Source", "Time", "SessionTime", "DriverNumber")
    DATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    SESSIONTIME_FIELD_NUMBER: _ClassVar[int]
    DRIVERNUMBER_FIELD_NUMBER: _ClassVar[int]
    Date: _timestamp_pb2.Timestamp
    Status: str
    X: int
    Y: int
    Z: int
    Source: str
    Time: _duration_pb2.Duration
    SessionTime: _duration_pb2.Duration
    DriverNumber: str
    def __init__(self, Date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., Status: _Optional[str] = ..., X: _Optional[int] = ..., Y: _Optional[int] = ..., Z: _Optional[int] = ..., Source: _Optional[str] = ..., Time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., SessionTime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., DriverNumber: _Optional[str] = ...) -> None: ...
