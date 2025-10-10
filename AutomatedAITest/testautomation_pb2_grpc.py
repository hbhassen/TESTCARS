"""gRPC stubs for the subset of PROVEtech:TA services used by AutomatedAITest."""
from __future__ import annotations

import grpc

import testautomation_pb2 as testautomation__pb2


class ApplicationStub:
    """Client stub for the Application service."""

    def __init__(self, channel: grpc.Channel) -> None:
        self.Init = channel.unary_unary(
            "/testautomation.Application/Init",
            request_serializer=testautomation__pb2.ApplicationInitRequest.SerializeToString,
            response_deserializer=testautomation__pb2.ApplicationInitReply.FromString,
        )


class SystemStub:
    """Client stub for the System service."""

    def __init__(self, channel: grpc.Channel) -> None:
        self.ModifyVideoAudioConfig = channel.unary_unary(
            "/testautomation.System/ModifyVideoAudioConfig",
            request_serializer=testautomation__pb2.SystemModifyVideoAudioConfigRequest.SerializeToString,
            response_deserializer=testautomation__pb2.SystemModifyVideoAudioConfigReply.FromString,
        )
        self.ModifyModelNodeConfig = channel.unary_unary(
            "/testautomation.System/ModifyModelNodeConfig",
            request_serializer=testautomation__pb2.SystemModifyModelNodeConfigRequest.SerializeToString,
            response_deserializer=testautomation__pb2.SystemModifyModelNodeConfigReply.FromString,
        )
        self.LoadModel = channel.unary_unary(
            "/testautomation.System/LoadModel",
            request_serializer=testautomation__pb2.SystemLoadModelRequest.SerializeToString,
            response_deserializer=testautomation__pb2.SystemLoadModelReply.FromString,
        )
        self.GetSignal = channel.unary_unary(
            "/testautomation.System/GetSignal",
            request_serializer=testautomation__pb2.SystemGetSignalRequest.SerializeToString,
            response_deserializer=testautomation__pb2.SystemGetSignalReply.FromString,
        )
        self.GetResult = channel.unary_unary(
            "/testautomation.System/GetResult",
            request_serializer=testautomation__pb2.SystemGetResultRequest.SerializeToString,
            response_deserializer=testautomation__pb2.SystemGetResultReply.FromString,
        )


class MeasureStub:
    """Client stub for the Measure service."""

    def __init__(self, channel: grpc.Channel) -> None:
        self.SetVideoAudio = channel.unary_unary(
            "/testautomation.Measure/SetVideoAudio",
            request_serializer=testautomation__pb2.MeasureSetVideoAudioRequest.SerializeToString,
            response_deserializer=testautomation__pb2.MeasureSetVideoAudioReply.FromString,
        )
        self.Start = channel.unary_unary(
            "/testautomation.Measure/Start",
            request_serializer=testautomation__pb2.MeasureStartRequest.SerializeToString,
            response_deserializer=testautomation__pb2.MeasureStartReply.FromString,
        )
        self.Stop = channel.unary_unary(
            "/testautomation.Measure/Stop",
            request_serializer=testautomation__pb2.MeasureStopRequest.SerializeToString,
            response_deserializer=testautomation__pb2.MeasureStopReply.FromString,
        )
        self.IsRunning = channel.unary_unary(
            "/testautomation.Measure/IsRunning",
            request_serializer=testautomation__pb2.MeasureIsRunningRequest.SerializeToString,
            response_deserializer=testautomation__pb2.MeasureIsRunningReply.FromString,
        )
        self.SaveFile = channel.unary_unary(
            "/testautomation.Measure/SaveFile",
            request_serializer=testautomation__pb2.MeasureSaveFileRequest.SerializeToString,
            response_deserializer=testautomation__pb2.MeasureSaveFileReply.FromString,
        )


class TestAutomationServiceStub:
    """High-level orchestration service exposed by PROVEtech:TA."""

    def __init__(self, channel: grpc.Channel) -> None:
        self.AddDevice = channel.unary_unary(
            "/testautomation.TestAutomationService/AddDevice",
            request_serializer=testautomation__pb2.DeviceConfiguration.SerializeToString,
            response_deserializer=testautomation__pb2.DeviceConfigurationReply.FromString,
        )
        self.SetVideoSource = channel.unary_unary(
            "/testautomation.TestAutomationService/SetVideoSource",
            request_serializer=testautomation__pb2.DeviceIdentifier.SerializeToString,
            response_deserializer=testautomation__pb2.VideoSourceReply.FromString,
        )
        self.SetConfiguration = channel.unary_unary(
            "/testautomation.TestAutomationService/SetConfiguration",
            request_serializer=testautomation__pb2.ConfigEntry.SerializeToString,
            response_deserializer=testautomation__pb2.ConfigEntryReply.FromString,
        )
        self.ActivateCommunication = channel.unary_unary(
            "/testautomation.TestAutomationService/ActivateCommunication",
            request_serializer=testautomation__pb2.CommunicationRequest.SerializeToString,
            response_deserializer=testautomation__pb2.CommunicationReply.FromString,
        )
        self.StartTesting = channel.unary_unary(
            "/testautomation.TestAutomationService/StartTesting",
            request_serializer=testautomation__pb2.StartTestRequest.SerializeToString,
            response_deserializer=testautomation__pb2.StartTestReply.FromString,
        )
        self.GetSignal = channel.unary_unary(
            "/testautomation.TestAutomationService/GetSignal",
            request_serializer=testautomation__pb2.SystemGetSignalRequest.SerializeToString,
            response_deserializer=testautomation__pb2.SystemGetSignalReply.FromString,
        )
        self.SaveResult = channel.unary_unary(
            "/testautomation.TestAutomationService/SaveResult",
            request_serializer=testautomation__pb2.ResultExportRequest.SerializeToString,
            response_deserializer=testautomation__pb2.ResultExportReply.FromString,
        )
        self.StopTesting = channel.unary_unary(
            "/testautomation.TestAutomationService/StopTesting",
            request_serializer=testautomation__pb2.StopTestRequest.SerializeToString,
            response_deserializer=testautomation__pb2.StopTestReply.FromString,
        )


__all__ = ["ApplicationStub", "SystemStub", "MeasureStub", "TestAutomationServiceStub"]
