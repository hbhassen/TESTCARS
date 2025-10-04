"""Simplified protobuf definitions for the AutomatedAITest workflow."""
from __future__ import annotations

from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2

_sym_db = _symbol_database.Default()


def _build_file_descriptor() -> None:
    file_proto = descriptor_pb2.FileDescriptorProto()
    file_proto.name = "testautomation.proto"
    file_proto.package = "testautomation"
    file_proto.syntax = "proto3"

    # SystemModifyVideoAudioConfigRequest
    msg = file_proto.message_type.add()
    msg.name = "SystemModifyVideoAudioConfigRequest"
    field = msg.field.add()
    field.name = "strSourceName"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "strConfig"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "strShareWithModelNode"
    field.number = 3
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "SystemModifyVideoAudioConfigReply"

    # SystemModifyModelNodeConfigRequest
    msg = file_proto.message_type.add()
    msg.name = "SystemModifyModelNodeConfigRequest"
    field = msg.field.add()
    field.name = "strModelNodeName"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "strConfig"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "lTimeoutInSeconds"
    field.number = 3
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT32

    msg = file_proto.message_type.add()
    msg.name = "SystemModifyModelNodeConfigReply"
    field = msg.field.add()
    field.name = "RetVal"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    # SystemLoadModel
    msg = file_proto.message_type.add()
    msg.name = "SystemLoadModelRequest"
    field = msg.field.add()
    field.name = "strModelName"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "SystemLoadModelReply"
    field = msg.field.add()
    field.name = "RetVal"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    # MeasureSetVideoAudio
    msg = file_proto.message_type.add()
    msg.name = "MeasureSetVideoAudioRequest"
    field = msg.field.add()
    field.name = "strName"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "bActivate"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    field = msg.field.add()
    field.name = "bPauseVideoInitially"
    field.number = 3
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    field = msg.field.add()
    field.name = "bPauseAudioInitially"
    field.number = 4
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    msg = file_proto.message_type.add()
    msg.name = "MeasureSetVideoAudioReply"
    field = msg.field.add()
    field.name = "RetVal"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    # MeasureStart / Stop / IsRunning
    msg = file_proto.message_type.add()
    msg.name = "MeasureStartRequest"
    field = msg.field.add()
    field.name = "bSaveToDisk"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    msg = file_proto.message_type.add()
    msg.name = "MeasureStartReply"
    field = msg.field.add()
    field.name = "RetVal"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    msg = file_proto.message_type.add()
    msg.name = "MeasureStopRequest"

    msg = file_proto.message_type.add()
    msg.name = "MeasureStopReply"
    field = msg.field.add()
    field.name = "RetVal"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    msg = file_proto.message_type.add()
    msg.name = "MeasureIsRunningRequest"

    msg = file_proto.message_type.add()
    msg.name = "MeasureIsRunningReply"
    field = msg.field.add()
    field.name = "RetVal"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    # SystemGetSignal
    msg = file_proto.message_type.add()
    msg.name = "SystemGetSignalRequest"
    field = msg.field.add()
    field.name = "strSignalName"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "bInterpreted"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    msg = file_proto.message_type.add()
    msg.name = "SystemGetSignalReply"
    oneof = msg.oneof_decl.add()
    oneof.name = "RetVal"
    field = msg.field.add()
    field.name = "RetVal_double"
    field.number = 31
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE
    field.oneof_index = 0
    field = msg.field.add()
    field.name = "RetVal_int64"
    field.number = 33
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT64
    field.oneof_index = 0
    field = msg.field.add()
    field.name = "RetVal_uint64"
    field.number = 35
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_UINT64
    field.oneof_index = 0
    field = msg.field.add()
    field.name = "RetVal_string"
    field.number = 40
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field.oneof_index = 0

    # SystemGetResult
    msg = file_proto.message_type.add()
    msg.name = "SystemGetResultRequest"

    msg = file_proto.message_type.add()
    msg.name = "SystemGetResultReply"
    field = msg.field.add()
    field.name = "RetVal"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT32
    field = msg.field.add()
    field.name = "piAdditionalResultValue"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT32
    field = msg.field.add()
    field.name = "pbAddResultToProtocol"
    field.number = 3
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    pool = _descriptor_pool.Default()
    pool.Add(file_proto)


_build_file_descriptor()

DESCRIPTOR = _descriptor_pool.Default().FindFileByName("testautomation.proto")

SystemModifyVideoAudioConfigRequest = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["SystemModifyVideoAudioConfigRequest"]
)
SystemModifyVideoAudioConfigReply = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["SystemModifyVideoAudioConfigReply"]
)
SystemModifyModelNodeConfigRequest = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["SystemModifyModelNodeConfigRequest"]
)
SystemModifyModelNodeConfigReply = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["SystemModifyModelNodeConfigReply"]
)
SystemLoadModelRequest = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["SystemLoadModelRequest"]
)
SystemLoadModelReply = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["SystemLoadModelReply"]
)
MeasureSetVideoAudioRequest = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["MeasureSetVideoAudioRequest"]
)
MeasureSetVideoAudioReply = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["MeasureSetVideoAudioReply"]
)
MeasureStartRequest = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["MeasureStartRequest"]
)
MeasureStartReply = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["MeasureStartReply"]
)
MeasureStopRequest = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["MeasureStopRequest"]
)
MeasureStopReply = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["MeasureStopReply"]
)
MeasureIsRunningRequest = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["MeasureIsRunningRequest"]
)
MeasureIsRunningReply = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["MeasureIsRunningReply"]
)
SystemGetSignalRequest = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["SystemGetSignalRequest"]
)
SystemGetSignalReply = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["SystemGetSignalReply"]
)
SystemGetResultRequest = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["SystemGetResultRequest"]
)
SystemGetResultReply = _sym_db.GetPrototype(
    DESCRIPTOR.message_types_by_name["SystemGetResultReply"]
)

__all__ = [
    "SystemModifyVideoAudioConfigRequest",
    "SystemModifyVideoAudioConfigReply",
    "SystemModifyModelNodeConfigRequest",
    "SystemModifyModelNodeConfigReply",
    "SystemLoadModelRequest",
    "SystemLoadModelReply",
    "MeasureSetVideoAudioRequest",
    "MeasureSetVideoAudioReply",
    "MeasureStartRequest",
    "MeasureStartReply",
    "MeasureStopRequest",
    "MeasureStopReply",
    "MeasureIsRunningRequest",
    "MeasureIsRunningReply",
    "SystemGetSignalRequest",
    "SystemGetSignalReply",
    "SystemGetResultRequest",
    "SystemGetResultReply",
]
