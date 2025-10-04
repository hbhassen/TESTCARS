"""gRPC stubs for the subset of PROVEtech:TA services used by AutomatedAITest."""
from __future__ import annotations

import grpc

import testautomation_pb2 as testautomation__pb2


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


__all__ = ["SystemStub", "MeasureStub"]
