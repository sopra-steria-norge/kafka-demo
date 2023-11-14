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

class WeatherData(_message.Message):
    __slots__ = ("Time", "AirTemp", "Humidity", "Pressure", "Rainfall", "TrackTemp", "WindDirection", "WindSpeed")
    TIME_FIELD_NUMBER: _ClassVar[int]
    AIRTEMP_FIELD_NUMBER: _ClassVar[int]
    HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_FIELD_NUMBER: _ClassVar[int]
    RAINFALL_FIELD_NUMBER: _ClassVar[int]
    TRACKTEMP_FIELD_NUMBER: _ClassVar[int]
    WINDDIRECTION_FIELD_NUMBER: _ClassVar[int]
    WINDSPEED_FIELD_NUMBER: _ClassVar[int]
    Time: _duration_pb2.Duration
    AirTemp: float
    Humidity: float
    Pressure: float
    Rainfall: bool
    TrackTemp: float
    WindDirection: int
    WindSpeed: float
    def __init__(self, Time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., AirTemp: _Optional[float] = ..., Humidity: _Optional[float] = ..., Pressure: _Optional[float] = ..., Rainfall: bool = ..., TrackTemp: _Optional[float] = ..., WindDirection: _Optional[int] = ..., WindSpeed: _Optional[float] = ...) -> None: ...

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

class SessionStatus(_message.Message):
    __slots__ = ("Time", "Status")
    TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    Time: _duration_pb2.Duration
    Status: str
    def __init__(self, Time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., Status: _Optional[str] = ...) -> None: ...

class TrackStatus(_message.Message):
    __slots__ = ("Time", "Status", "Message")
    TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    Time: _duration_pb2.Duration
    Status: str
    Message: str
    def __init__(self, Time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., Status: _Optional[str] = ..., Message: _Optional[str] = ...) -> None: ...

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
