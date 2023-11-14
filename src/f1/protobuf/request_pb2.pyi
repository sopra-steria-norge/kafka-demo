from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Identifiers(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RACE: _ClassVar[Identifiers]
    QUALIFYING: _ClassVar[Identifiers]
    SPRINT: _ClassVar[Identifiers]
    SPRINT_QUALIFYING: _ClassVar[Identifiers]
    SPRINT_SHOOTOUT: _ClassVar[Identifiers]
    PRACTICE_1: _ClassVar[Identifiers]
    PRACTICE_2: _ClassVar[Identifiers]
    PRACTICE_3: _ClassVar[Identifiers]

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SENDT: _ClassVar[Status]
    RECIVED: _ClassVar[Status]
    STARTED: _ClassVar[Status]
    COMPLETED: _ClassVar[Status]
    SIMULATING: _ClassVar[Status]
RACE: Identifiers
QUALIFYING: Identifiers
SPRINT: Identifiers
SPRINT_QUALIFYING: Identifiers
SPRINT_SHOOTOUT: Identifiers
PRACTICE_1: Identifiers
PRACTICE_2: Identifiers
PRACTICE_3: Identifiers
SENDT: Status
RECIVED: Status
STARTED: Status
COMPLETED: Status
SIMULATING: Status

class RequestSession(_message.Message):
    __slots__ = ("Year", "GrandPrix", "Identifier", "PositionData", "CarData")
    YEAR_FIELD_NUMBER: _ClassVar[int]
    GRANDPRIX_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    POSITIONDATA_FIELD_NUMBER: _ClassVar[int]
    CARDATA_FIELD_NUMBER: _ClassVar[int]
    Year: int
    GrandPrix: int
    Identifier: Identifiers
    PositionData: bool
    CarData: bool
    def __init__(self, Year: _Optional[int] = ..., GrandPrix: _Optional[int] = ..., Identifier: _Optional[_Union[Identifiers, str]] = ..., PositionData: bool = ..., CarData: bool = ...) -> None: ...

class SessionStatusResponse(_message.Message):
    __slots__ = ("Time", "Status")
    TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    Time: _timestamp_pb2.Timestamp
    Status: Status
    def __init__(self, Time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., Status: _Optional[_Union[Status, str]] = ...) -> None: ...
