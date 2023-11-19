# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/laps.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13protobuf/laps.proto\x12\x16\x63ompany.proto.formula1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\"\xb5\x07\n\x04Laps\x12\'\n\x04Time\x18\x01 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x0e\n\x06\x44river\x18\x02 \x01(\t\x12\x14\n\x0c\x44riverNumber\x18\x03 \x01(\t\x12*\n\x07LapTime\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x11\n\tLapNumber\x18\x05 \x01(\x02\x12\r\n\x05Stint\x18\x06 \x01(\x02\x12-\n\nPitOutTime\x18\x07 \x01(\x0b\x32\x19.google.protobuf.Duration\x12,\n\tPitInTime\x18\x08 \x01(\x0b\x32\x19.google.protobuf.Duration\x12.\n\x0bSector1Time\x18\t \x01(\x0b\x32\x19.google.protobuf.Duration\x12.\n\x0bSector2Time\x18\n \x01(\x0b\x32\x19.google.protobuf.Duration\x12.\n\x0bSector3Time\x18\x0b \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x35\n\x12Sector1SessionTime\x18\x0c \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x35\n\x12Sector2SessionTime\x18\r \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x35\n\x12Sector3SessionTime\x18\x0e \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x0f\n\x07SpeedI1\x18\x0f \x01(\x02\x12\x0f\n\x07SpeedI2\x18\x10 \x01(\x02\x12\x0f\n\x07SpeedFL\x18\x11 \x01(\x02\x12\x0f\n\x07SpeedST\x18\x12 \x01(\x02\x12\x16\n\x0eIsPersonalBest\x18\x13 \x01(\x08\x12\x10\n\x08\x43ompound\x18\x14 \x01(\t\x12\x10\n\x08TyreLife\x18\x15 \x01(\x02\x12\x11\n\tFreshTyre\x18\x16 \x01(\x08\x12\x0c\n\x04Team\x18\x17 \x01(\t\x12/\n\x0cLapStartTime\x18\x18 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x30\n\x0cLapStartDate\x18\x19 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0bTrackStatus\x18\x1a \x01(\t\x12\x10\n\x08Position\x18\x1b \x01(\x02\x12\x0f\n\x07\x44\x65leted\x18\x1c \x01(\x08\x12\x15\n\rDeletedReason\x18\x1d \x01(\t\x12\x17\n\x0f\x46\x61stF1Generated\x18\x1e \x01(\x08\x12\x12\n\nIsAccurate\x18\x1f \x01(\x08\x42!\xaa\x02\x1e\x43ompany.Proto.Formula1.Sessionb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protobuf.laps_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002\036Company.Proto.Formula1.Session'
  _globals['_LAPS']._serialized_start=113
  _globals['_LAPS']._serialized_end=1062
# @@protoc_insertion_point(module_scope)
