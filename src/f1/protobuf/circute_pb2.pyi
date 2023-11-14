from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CircuitInfo(_message.Message):
    __slots__ = ("Corners", "MarshalLights", "MarshalSectors", "Rotation")
    CORNERS_FIELD_NUMBER: _ClassVar[int]
    MARSHALLIGHTS_FIELD_NUMBER: _ClassVar[int]
    MARSHALSECTORS_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    Corners: _containers.RepeatedCompositeFieldContainer[TrackMarkers]
    MarshalLights: _containers.RepeatedCompositeFieldContainer[TrackMarkers]
    MarshalSectors: _containers.RepeatedCompositeFieldContainer[TrackMarkers]
    Rotation: float
    def __init__(self, Corners: _Optional[_Iterable[_Union[TrackMarkers, _Mapping]]] = ..., MarshalLights: _Optional[_Iterable[_Union[TrackMarkers, _Mapping]]] = ..., MarshalSectors: _Optional[_Iterable[_Union[TrackMarkers, _Mapping]]] = ..., Rotation: _Optional[float] = ...) -> None: ...

class TrackMarkers(_message.Message):
    __slots__ = ("X", "Y", "Number", "Letter", "Angle", "Distance")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    LETTER_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    X: float
    Y: float
    Number: int
    Letter: str
    Angle: float
    Distance: float
    def __init__(self, X: _Optional[float] = ..., Y: _Optional[float] = ..., Number: _Optional[int] = ..., Letter: _Optional[str] = ..., Angle: _Optional[float] = ..., Distance: _Optional[float] = ...) -> None: ...
