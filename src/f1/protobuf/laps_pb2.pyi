from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Laps(_message.Message):
    __slots__ = ("Time", "Driver", "DriverNumber", "LapTime", "LapNumber", "Stint", "PitOutTime", "PitInTime", "Sector1Time", "Sector2Time", "Sector3Time", "Sector1SessionTime", "Sector2SessionTime", "Sector3SessionTime", "SpeedI1", "SpeedI2", "SpeedFL", "SpeedST", "IsPersonalBest", "Compound", "TyreLife", "FreshTyre", "Team", "LapStartTime", "LapStartDate", "TrackStatus", "Position", "Deleted", "DeletedReason", "FastF1Generated", "IsAccurate")
    TIME_FIELD_NUMBER: _ClassVar[int]
    DRIVER_FIELD_NUMBER: _ClassVar[int]
    DRIVERNUMBER_FIELD_NUMBER: _ClassVar[int]
    LAPTIME_FIELD_NUMBER: _ClassVar[int]
    LAPNUMBER_FIELD_NUMBER: _ClassVar[int]
    STINT_FIELD_NUMBER: _ClassVar[int]
    PITOUTTIME_FIELD_NUMBER: _ClassVar[int]
    PITINTIME_FIELD_NUMBER: _ClassVar[int]
    SECTOR1TIME_FIELD_NUMBER: _ClassVar[int]
    SECTOR2TIME_FIELD_NUMBER: _ClassVar[int]
    SECTOR3TIME_FIELD_NUMBER: _ClassVar[int]
    SECTOR1SESSIONTIME_FIELD_NUMBER: _ClassVar[int]
    SECTOR2SESSIONTIME_FIELD_NUMBER: _ClassVar[int]
    SECTOR3SESSIONTIME_FIELD_NUMBER: _ClassVar[int]
    SPEEDI1_FIELD_NUMBER: _ClassVar[int]
    SPEEDI2_FIELD_NUMBER: _ClassVar[int]
    SPEEDFL_FIELD_NUMBER: _ClassVar[int]
    SPEEDST_FIELD_NUMBER: _ClassVar[int]
    ISPERSONALBEST_FIELD_NUMBER: _ClassVar[int]
    COMPOUND_FIELD_NUMBER: _ClassVar[int]
    TYRELIFE_FIELD_NUMBER: _ClassVar[int]
    FRESHTYRE_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    LAPSTARTTIME_FIELD_NUMBER: _ClassVar[int]
    LAPSTARTDATE_FIELD_NUMBER: _ClassVar[int]
    TRACKSTATUS_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DELETED_FIELD_NUMBER: _ClassVar[int]
    DELETEDREASON_FIELD_NUMBER: _ClassVar[int]
    FASTF1GENERATED_FIELD_NUMBER: _ClassVar[int]
    ISACCURATE_FIELD_NUMBER: _ClassVar[int]
    Time: _duration_pb2.Duration
    Driver: str
    DriverNumber: str
    LapTime: _duration_pb2.Duration
    LapNumber: float
    Stint: float
    PitOutTime: _duration_pb2.Duration
    PitInTime: _duration_pb2.Duration
    Sector1Time: _duration_pb2.Duration
    Sector2Time: _duration_pb2.Duration
    Sector3Time: _duration_pb2.Duration
    Sector1SessionTime: _duration_pb2.Duration
    Sector2SessionTime: _duration_pb2.Duration
    Sector3SessionTime: _duration_pb2.Duration
    SpeedI1: float
    SpeedI2: float
    SpeedFL: float
    SpeedST: float
    IsPersonalBest: bool
    Compound: str
    TyreLife: float
    FreshTyre: bool
    Team: str
    LapStartTime: _duration_pb2.Duration
    LapStartDate: _timestamp_pb2.Timestamp
    TrackStatus: str
    Position: float
    Deleted: bool
    DeletedReason: str
    FastF1Generated: bool
    IsAccurate: bool
    def __init__(self, Time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., Driver: _Optional[str] = ..., DriverNumber: _Optional[str] = ..., LapTime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., LapNumber: _Optional[float] = ..., Stint: _Optional[float] = ..., PitOutTime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., PitInTime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., Sector1Time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., Sector2Time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., Sector3Time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., Sector1SessionTime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., Sector2SessionTime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., Sector3SessionTime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., SpeedI1: _Optional[float] = ..., SpeedI2: _Optional[float] = ..., SpeedFL: _Optional[float] = ..., SpeedST: _Optional[float] = ..., IsPersonalBest: bool = ..., Compound: _Optional[str] = ..., TyreLife: _Optional[float] = ..., FreshTyre: bool = ..., Team: _Optional[str] = ..., LapStartTime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., LapStartDate: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., TrackStatus: _Optional[str] = ..., Position: _Optional[float] = ..., Deleted: bool = ..., DeletedReason: _Optional[str] = ..., FastF1Generated: bool = ..., IsAccurate: bool = ...) -> None: ...
