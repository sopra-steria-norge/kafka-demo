from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CarData(_message.Message):
    __slots__ = ("Date", "RPM", "Speed", "nGear", "Throttle", "Brake", "DRS", "Source", "Time", "SessionTime", "DrvierNumber")
    DATE_FIELD_NUMBER: _ClassVar[int]
    RPM_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    NGEAR_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_FIELD_NUMBER: _ClassVar[int]
    BRAKE_FIELD_NUMBER: _ClassVar[int]
    DRS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    SESSIONTIME_FIELD_NUMBER: _ClassVar[int]
    DRVIERNUMBER_FIELD_NUMBER: _ClassVar[int]
    Date: _timestamp_pb2.Timestamp
    RPM: int
    Speed: int
    nGear: int
    Throttle: int
    Brake: bool
    DRS: int
    Source: str
    Time: _duration_pb2.Duration
    SessionTime: _duration_pb2.Duration
    DrvierNumber: str
    def __init__(self, Date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., RPM: _Optional[int] = ..., Speed: _Optional[int] = ..., nGear: _Optional[int] = ..., Throttle: _Optional[int] = ..., Brake: bool = ..., DRS: _Optional[int] = ..., Source: _Optional[str] = ..., Time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., SessionTime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., DrvierNumber: _Optional[str] = ...) -> None: ...
