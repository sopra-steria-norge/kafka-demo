from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

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
