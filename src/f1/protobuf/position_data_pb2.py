# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/position_data.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cprotobuf/position_data.proto\x12\x16\x63ompany.proto.formula1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\"\xe8\x01\n\x0cPositionData\x12(\n\x04\x44\x61te\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06Status\x18\x02 \x01(\t\x12\t\n\x01X\x18\x03 \x01(\x03\x12\t\n\x01Y\x18\x04 \x01(\x03\x12\t\n\x01Z\x18\x05 \x01(\x03\x12\x0e\n\x06Source\x18\x06 \x01(\t\x12\'\n\x04Time\x18\x07 \x01(\x0b\x32\x19.google.protobuf.Duration\x12.\n\x0bSessionTime\x18\x08 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x14\n\x0c\x44riverNumber\x18\t \x01(\tB!\xaa\x02\x1e\x43ompany.Proto.Formula1.Sessionb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protobuf.position_data_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002\036Company.Proto.Formula1.Session'
  _globals['_POSITIONDATA']._serialized_start=122
  _globals['_POSITIONDATA']._serialized_end=354
# @@protoc_insertion_point(module_scope)
