"""Simplified protobuf definitions for the AutomatedAITest workflow."""
from __future__ import annotations

from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
from google.protobuf import message_factory as _message_factory

_sym_db = _symbol_database.Default()


def _build_file_descriptor() -> None:
    file_proto = descriptor_pb2.FileDescriptorProto()
    file_proto.name = "testautomation.proto"
    file_proto.package = "testautomation"
    file_proto.syntax = "proto3"

    # ApplicationInit
    msg = file_proto.message_type.add()
    msg.name = "ApplicationInitRequest"

    msg = file_proto.message_type.add()
    msg.name = "ApplicationInitReply"

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

    # MeasureSaveFile
    msg = file_proto.message_type.add()
    msg.name = "MeasureSaveFileRequest"
    field = msg.field.add()
    field.name = "strLabel"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "strType"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "strFileName"
    field.number = 3
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "MeasureSaveFileReply"
    field = msg.field.add()
    field.name = "RetVal"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    # Device workflow messages
    msg = file_proto.message_type.add()
    msg.name = "DeviceConfiguration"
    field = msg.field.add()
    field.name = "name"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "driver_id"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "type"
    field.number = 3
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "resolution"
    field.number = 4
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "enable"
    field.number = 5
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    field = msg.field.add()
    field.name = "webcam_index"
    field.number = 6
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT32

    msg = file_proto.message_type.add()
    msg.name = "DeviceConfigurationReply"
    field = msg.field.add()
    field.name = "success"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    field = msg.field.add()
    field.name = "message"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "DeviceIdentifier"
    field = msg.field.add()
    field.name = "name"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "VideoSourceReply"
    field = msg.field.add()
    field.name = "success"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    field = msg.field.add()
    field.name = "message"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "ConfigEntry"
    field = msg.field.add()
    field.name = "key"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    field = msg.field.add()
    field.name = "value"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "ConfigEntryReply"
    field = msg.field.add()
    field.name = "success"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    field = msg.field.add()
    field.name = "message"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "CommunicationRequest"
    field = msg.field.add()
    field.name = "enable"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

    msg = file_proto.message_type.add()
    msg.name = "CommunicationReply"
    field = msg.field.add()
    field.name = "success"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    field = msg.field.add()
    field.name = "message"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "StartTestRequest"
    field = msg.field.add()
    field.name = "model"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "StartTestReply"
    field = msg.field.add()
    field.name = "success"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    field = msg.field.add()
    field.name = "message"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "ResultExportRequest"
    field = msg.field.add()
    field.name = "path"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "ResultExportReply"
    field = msg.field.add()
    field.name = "success"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    field = msg.field.add()
    field.name = "message"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    msg = file_proto.message_type.add()
    msg.name = "StopTestRequest"

    msg = file_proto.message_type.add()
    msg.name = "StopTestReply"
    field = msg.field.add()
    field.name = "success"
    field.number = 1
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    field = msg.field.add()
    field.name = "message"
    field.number = 2
    field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    pool = _descriptor_pool.Default()
    pool.Add(file_proto)


_build_file_descriptor()

DESCRIPTOR = _descriptor_pool.Default().FindFileByName("testautomation.proto")


def _get_message_class(message_name: str):
    """Return the generated message class for ``message_name``.

    ``GetPrototype`` was removed from :mod:`google.protobuf` in v5+.  The
    helper keeps compatibility with older versions while supporting the
    modern :func:`google.protobuf.message_factory.GetMessageClass` helper.
    """

    message_descriptor = DESCRIPTOR.message_types_by_name[message_name]

    if hasattr(_sym_db, "GetPrototype"):
        return _sym_db.GetPrototype(message_descriptor)

    message_cls = _message_factory.GetMessageClass(message_descriptor)
    _sym_db.RegisterMessage(message_cls)
    return message_cls


ApplicationInitRequest = _get_message_class("ApplicationInitRequest")
ApplicationInitReply = _get_message_class("ApplicationInitReply")
SystemModifyVideoAudioConfigRequest = _get_message_class(
    "SystemModifyVideoAudioConfigRequest"
)
SystemModifyVideoAudioConfigReply = _get_message_class(
    "SystemModifyVideoAudioConfigReply"
)
SystemModifyModelNodeConfigRequest = _get_message_class(
    "SystemModifyModelNodeConfigRequest"
)
SystemModifyModelNodeConfigReply = _get_message_class(
    "SystemModifyModelNodeConfigReply"
)
SystemLoadModelRequest = _get_message_class("SystemLoadModelRequest")
SystemLoadModelReply = _get_message_class("SystemLoadModelReply")
MeasureSetVideoAudioRequest = _get_message_class("MeasureSetVideoAudioRequest")
MeasureSetVideoAudioReply = _get_message_class("MeasureSetVideoAudioReply")
MeasureStartRequest = _get_message_class("MeasureStartRequest")
MeasureStartReply = _get_message_class("MeasureStartReply")
MeasureStopRequest = _get_message_class("MeasureStopRequest")
MeasureStopReply = _get_message_class("MeasureStopReply")
MeasureIsRunningRequest = _get_message_class("MeasureIsRunningRequest")
MeasureIsRunningReply = _get_message_class("MeasureIsRunningReply")
SystemGetSignalRequest = _get_message_class("SystemGetSignalRequest")
SystemGetSignalReply = _get_message_class("SystemGetSignalReply")
SystemGetResultRequest = _get_message_class("SystemGetResultRequest")
SystemGetResultReply = _get_message_class("SystemGetResultReply")
MeasureSaveFileRequest = _get_message_class("MeasureSaveFileRequest")
MeasureSaveFileReply = _get_message_class("MeasureSaveFileReply")
DeviceConfiguration = _get_message_class("DeviceConfiguration")
DeviceConfigurationReply = _get_message_class("DeviceConfigurationReply")
DeviceIdentifier = _get_message_class("DeviceIdentifier")
VideoSourceReply = _get_message_class("VideoSourceReply")
ConfigEntry = _get_message_class("ConfigEntry")
ConfigEntryReply = _get_message_class("ConfigEntryReply")
CommunicationRequest = _get_message_class("CommunicationRequest")
CommunicationReply = _get_message_class("CommunicationReply")
StartTestRequest = _get_message_class("StartTestRequest")
StartTestReply = _get_message_class("StartTestReply")
ResultExportRequest = _get_message_class("ResultExportRequest")
ResultExportReply = _get_message_class("ResultExportReply")
StopTestRequest = _get_message_class("StopTestRequest")
StopTestReply = _get_message_class("StopTestReply")

__all__ = [
    "ApplicationInitRequest",
    "ApplicationInitReply",
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
    "MeasureSaveFileRequest",
    "MeasureSaveFileReply",
    "DeviceConfiguration",
    "DeviceConfigurationReply",
    "DeviceIdentifier",
    "VideoSourceReply",
    "ConfigEntry",
    "ConfigEntryReply",
    "CommunicationRequest",
    "CommunicationReply",
    "StartTestRequest",
    "StartTestReply",
    "ResultExportRequest",
    "ResultExportReply",
    "StopTestRequest",
    "StopTestReply",
]
