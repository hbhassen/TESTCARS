"""Main entry point for the AutomatedAITest application."""
from __future__ import annotations

import argparse
import json
import math
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import grpc
import pandas as pd

from utils.logger import setup_logging, update_log_level

import testautomation_pb2 as ta_pb2
import testautomation_pb2_grpc as ta_grpc

# Default timeout used for gRPC invocations unless overridden in the
# configuration file or via CLI arguments.
DEFAULT_TIMEOUT_MS = 10000


class ConfigurationError(Exception):
    """Raised when the provided configuration is invalid."""


class ProcessLaunchError(Exception):
    """Raised when an external process such as PROVEtech:TA fails to launch."""


@dataclass
class GrpcSettings:
    """Connection settings for the PROVEtech:TA gRPC endpoint."""

    host: str
    port: int

    @property
    def endpoint(self) -> str:
        return f"{self.host}:{self.port}"


@dataclass
class AiCoreSettings:
    """Runtime configuration for AI-Core integration."""

    executable: Path
    config_file: Path
    timeout_ms: int
    parallel_instances: int


@dataclass
class VideoSettings:
    """Video pipeline configuration used for AI-Core processing."""

    device_name: str
    driver_id: str
    resolution: str
    mode: str = "device"
    file_path: Optional[Path] = None
    webcam_index: Optional[int] = None
    loop_file: bool = False


@dataclass
class LoggingSettings:
    """Logging configuration for the automation script."""

    level: str
    file: Path


@dataclass
class TestSettings:
    """Test execution specific parameters."""

    model_name: str
    ta_executable: Optional[Path]
    output_dir: Path
    log_signals: List[str] = field(default_factory=list)


@dataclass
class AutomationConfig:
    """Container for all configuration sections."""

    grpc: GrpcSettings
    ai_core: AiCoreSettings
    video: VideoSettings
    test: TestSettings
    logging: LoggingSettings

    @property
    def timeout_ms(self) -> int:
        return self.ai_core.timeout_ms or DEFAULT_TIMEOUT_MS


def _parse_scalar(value: str) -> Any:
    """Parse a scalar YAML value without requiring an external dependency."""

    value = value.strip()
    if not value:
        return ""
    if value.startswith("\"") and value.endswith("\""):
        return value[1:-1]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        return value


def _load_yaml(path: Path) -> Dict[str, Any]:
    """Minimal YAML parser supporting the subset required for config.yaml."""

    lines = path.read_text(encoding="utf-8").splitlines()
    data: Dict[str, Any] = {}
    stack: List[tuple[int, Any]] = [(-1, data)]

    index = 0
    total_lines = len(lines)
    while index < total_lines:
        raw_line = lines[index]
        index += 1
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        while stack and indent <= stack[-1][0] and len(stack) > 1:
            stack.pop()
        container = stack[-1][1]
        if stripped.startswith("- "):
            if not isinstance(container, list):
                raise ConfigurationError(
                    f"Invalid list placement at line {index}: {raw_line!r}"
                )
            container.append(_parse_scalar(stripped[2:]))
            continue
        if ":" not in stripped:
            raise ConfigurationError(f"Invalid configuration line: {raw_line!r}")
        key, value_part = stripped.split(":", 1)
        key = key.strip()
        value_part = value_part.strip()
        if value_part:
            if not isinstance(container, dict):
                raise ConfigurationError(
                    f"Unexpected scalar value under non-dict container: {raw_line!r}"
                )
            container[key] = _parse_scalar(value_part)
            continue
        # Determine if upcoming block is list or dict by peeking ahead.
        next_is_list = False
        peek_index = index
        while peek_index < total_lines:
            peek_line = lines[peek_index]
            peek_stripped = peek_line.strip()
            if not peek_stripped or peek_stripped.startswith("#"):
                peek_index += 1
                continue
            peek_indent = len(peek_line) - len(peek_line.lstrip(" "))
            if peek_indent <= indent:
                break
            next_is_list = peek_stripped.startswith("- ")
            break
        if not isinstance(container, dict):
            raise ConfigurationError(
                f"Cannot create nested structure for line: {raw_line!r}"
            )
        new_container: Any = [] if next_is_list else {}
        container[key] = new_container
        stack.append((indent, new_container))
    return data


def load_configuration(config_path: Path) -> AutomationConfig:
    """Load and validate the automation configuration from disk."""

    if not config_path.exists():
        raise ConfigurationError(f"Configuration file not found: {config_path}")
    raw = _load_yaml(config_path)

    try:
        grpc_cfg = raw["grpc"]
        ai_core_cfg = raw["ai_core"]
        video_cfg = raw["video"]
        test_cfg = raw["test"]
        logging_cfg = raw["logging"]
    except KeyError as exc:
        raise ConfigurationError(
            f"Missing configuration section: {exc.args[0]}"
        ) from exc

    grpc_settings = GrpcSettings(
        host=str(grpc_cfg.get("host", "localhost")),
        port=int(grpc_cfg.get("port", 50051)),
    )

    ai_core_settings = AiCoreSettings(
        executable=Path(str(ai_core_cfg.get("executable", ""))),
        config_file=Path(str(ai_core_cfg.get("config_file", ""))),
        timeout_ms=int(ai_core_cfg.get("timeout_ms", DEFAULT_TIMEOUT_MS)),
        parallel_instances=int(ai_core_cfg.get("parallel_instances", 1)),
    )

    video_mode = str(video_cfg.get("mode", "device")).lower()
    file_path_value = video_cfg.get("file_path")
    file_path = Path(str(file_path_value)) if file_path_value else None
    webcam_index_value = video_cfg.get("webcam_index")
    webcam_index = (
        int(webcam_index_value)
        if webcam_index_value not in (None, "", [])
        else None
    )
    loop_file = bool(video_cfg.get("loop_file", False))

    video_settings = VideoSettings(
        device_name=str(video_cfg.get("device_name", "")),
        driver_id=str(video_cfg.get("driver_id", "")),
        resolution=str(video_cfg.get("resolution", "")),
        mode=video_mode,
        file_path=file_path,
        webcam_index=webcam_index,
        loop_file=loop_file,
    )

    test_settings = TestSettings(
        model_name=str(test_cfg.get("model_name", "")),
        ta_executable=Path(test_cfg["ta_executable"]).expanduser()
        if "ta_executable" in test_cfg and test_cfg["ta_executable"]
        else None,
        output_dir=Path(str(test_cfg.get("output_dir", "./results"))),
        log_signals=[str(sig) for sig in test_cfg.get("log_signals", [])],
    )

    logging_settings = LoggingSettings(
        level=str(logging_cfg.get("level", "INFO")),
        file=Path(str(logging_cfg.get("file", "./logs/automation.log"))),
    )

    return AutomationConfig(
        grpc=grpc_settings,
        ai_core=ai_core_settings,
        video=video_settings,
        test=test_settings,
        logging=logging_settings,
    )


def apply_cli_overrides(config: AutomationConfig, args: argparse.Namespace) -> None:
    """Apply CLI overrides to the loaded configuration."""

    if args.grpc_host:
        config.grpc.host = args.grpc_host
    if args.grpc_port:
        config.grpc.port = args.grpc_port
    if args.model:
        config.test.model_name = args.model
    if args.video_source:
        config.video.device_name = args.video_source
    if args.video_driver:
        config.video.driver_id = args.video_driver
    if args.resolution:
        config.video.resolution = args.resolution
    if args.video_mode:
        config.video.mode = args.video_mode.lower()
    if args.video_file:
        config.video.file_path = Path(args.video_file)
    if args.webcam_index is not None:
        config.video.webcam_index = args.webcam_index
    if args.loop_video is not None:
        config.video.loop_file = args.loop_video
    if args.timeout:
        config.ai_core.timeout_ms = args.timeout
    if args.ai_core_config:
        config.ai_core.config_file = Path(args.ai_core_config)
    if args.ai_core_executable:
        config.ai_core.executable = Path(args.ai_core_executable)
    if args.output_dir:
        config.test.output_dir = Path(args.output_dir)
    if args.ta_executable:
        config.test.ta_executable = Path(args.ta_executable)
    if args.log_signal:
        config.test.log_signals = list(args.log_signal)
    if args.log_level:
        config.logging.level = args.log_level


def parse_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description="Automated AI test runner")
    parser.add_argument("--config", type=str, help="Path to configuration YAML")
    parser.add_argument("--grpc-host", dest="grpc_host", type=str, help="Override gRPC host")
    parser.add_argument("--grpc-port", dest="grpc_port", type=int, help="Override gRPC port")
    parser.add_argument("--model", type=str, help="Detection model name to load")
    parser.add_argument("--video-source", dest="video_source", type=str, help="Video source name")
    parser.add_argument("--video-driver", dest="video_driver", type=str, help="Driver identifier")
    parser.add_argument("--resolution", type=str, help="Video resolution (e.g. 1920x1080)")
    parser.add_argument(
        "--video-mode",
        dest="video_mode",
        choices=["device", "webcam", "file"],
        help="Video ingestion mode: physical device, PC webcam, or recorded file",
    )
    parser.add_argument(
        "--video-file",
        dest="video_file",
        type=str,
        help="Path to recorded video when using file mode",
    )
    parser.add_argument(
        "--webcam-index",
        dest="webcam_index",
        type=int,
        help="Numeric index of the local webcam to bind when using webcam mode",
    )
    parser.add_argument(
        "--loop-video",
        dest="loop_video",
        action="store_true",
        help="Loop recorded video playback",
    )
    parser.add_argument(
        "--no-loop-video",
        dest="loop_video",
        action="store_false",
        help="Disable recorded video looping",
    )
    parser.add_argument("--timeout", type=int, help="RPC timeout in milliseconds")
    parser.add_argument("--ai-core-config", dest="ai_core_config", type=str, help="AI-Core configuration file path")
    parser.add_argument("--ai-core-executable", dest="ai_core_executable", type=str, help="AI-Core executable path")
    parser.add_argument("--output-dir", dest="output_dir", type=str, help="Directory for test results")
    parser.add_argument("--log-signal", dest="log_signal", action="append", help="Signals to monitor (can be used multiple times)")
    parser.add_argument("--log-level", dest="log_level", type=str, help="Override logging level")
    parser.add_argument("--ta-executable", dest="ta_executable", type=str, help="Path to PROVEtech:TA executable")
    parser.add_argument("--skip-ta-launch", action="store_true", help="Do not launch PROVEtech:TA from the script")
    parser.add_argument("--monitor-seconds", dest="monitor_seconds", type=int, help="Maximum monitoring duration in seconds")
    parser.add_argument("--poll-interval", dest="poll_interval", type=float, default=0.5, help="Signal polling interval in seconds")
    parser.add_argument("--no-ai-core-launch", dest="skip_ai_core", action="store_true", help="Skip launching AI-Core executable")
    parser.set_defaults(loop_video=None)
    return parser.parse_args(argv)


def _terminate_process(process: subprocess.Popen[bytes], logger) -> None:
    """Terminate a spawned subprocess gracefully."""

    if process.poll() is not None:
        return
    logger.info("Terminating process PID %s", process.pid)
    if os.name == "nt":
        process.send_signal(signal.CTRL_BREAK_EVENT)  # type: ignore[attr-defined]
        try:
            process.wait(timeout=5)
            return
        except subprocess.TimeoutExpired:
            process.terminate()
    else:
        process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        logger.warning("Process PID %s did not terminate, killing", process.pid)
        process.kill()


def start_process(executable: Path, arguments: Iterable[str], logger) -> subprocess.Popen[bytes]:
    """Launch an external process and ensure it starts correctly."""

    if not executable.exists():
        raise ProcessLaunchError(f"Executable not found: {executable}")
    cmd = [str(executable), *arguments]
    logger.info("Launching process: %s", " ".join(cmd))
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore[attr-defined]
    try:
        return subprocess.Popen(cmd, creationflags=creationflags)
    except OSError as exc:
        raise ProcessLaunchError(f"Failed to launch {executable}: {exc}") from exc


class TestAutomationController:
    """High level orchestration of the PROVEtech:TA automation workflow."""

    def __init__(self, config: AutomationConfig, logger) -> None:
        self.config = config
        self.logger = logger
        self.channel: Optional[grpc.Channel] = None
        self.system_stub: Optional[ta_grpc.SystemStub] = None
        self.measure_stub: Optional[ta_grpc.MeasureStub] = None

    def connect(self) -> None:
        """Connect to the PROVEtech:TA gRPC endpoint."""

        endpoint = self.config.grpc.endpoint
        self.logger.info("Connecting to PROVEtech:TA gRPC endpoint at %s", endpoint)
        options = [
            ("grpc.keepalive_time_ms", 10000),
            ("grpc.keepalive_timeout_ms", 5000),
        ]
        channel = grpc.insecure_channel(endpoint, options=options)
        deadline = time.time() + max(self.config.timeout_ms / 1000.0, 5)
        try:
            grpc.channel_ready_future(channel).result(timeout=deadline - time.time())
        except Exception as exc:  # pragma: no cover - network heavy
            raise ConnectionError(f"Unable to connect to {endpoint}: {exc}") from exc
        self.channel = channel
        self.system_stub = ta_grpc.SystemStub(channel)
        self.measure_stub = ta_grpc.MeasureStub(channel)
        self.logger.info("Successfully connected to %s", endpoint)

    def configure_video(self) -> None:
        """Configure the video device and link it to AI-Core."""

        assert self.system_stub is not None and self.measure_stub is not None
        video = self.config.video
        mode = video.mode.lower()
        if mode not in {"device", "webcam", "file"}:
            raise ConfigurationError(f"Unsupported video mode: {video.mode}")
        self.logger.info(
            "Configuring video source %s (%s) at resolution %s in %s mode",
            video.device_name,
            video.driver_id,
            video.resolution,
            mode,
        )
        config_payload = {
            "device_name": video.device_name,
            "driver_id": video.driver_id,
            "resolution": video.resolution,
            "share_with_model": self.config.test.model_name,
            "mode": mode,
        }
        if mode == "webcam" and video.webcam_index is not None:
            config_payload["webcam_index"] = video.webcam_index
        if mode == "file":
            if video.file_path is None:
                raise ConfigurationError("Video file path must be provided when mode is 'file'")
            file_path = video.file_path.expanduser()
            if not file_path.exists():
                raise ConfigurationError(f"Configured video file does not exist: {file_path}")
            config_payload["file_path"] = str(file_path)
            config_payload["loop_file"] = video.loop_file
        request = ta_pb2.SystemModifyVideoAudioConfigRequest(
            strSourceName=video.device_name,
            strConfig=json.dumps(config_payload),
            strShareWithModelNode=self.config.test.model_name,
        )
        self._call_rpc(
            self.system_stub.ModifyVideoAudioConfig,
            request,
            "ModifyVideoAudioConfig",
        )

        measure_request = ta_pb2.MeasureSetVideoAudioRequest(
            strName=video.device_name,
            bActivate=True,
            bPauseVideoInitially=False,
            bPauseAudioInitially=False,
        )
        self._call_rpc(
            self.measure_stub.SetVideoAudio,
            measure_request,
            "SetVideoAudio",
        )

    def configure_ai_core(self) -> None:
        """Configure the AI-Core executable and project file."""

        assert self.system_stub is not None
        ai_core = self.config.ai_core
        timeout_seconds = math.ceil(ai_core.timeout_ms / 1000.0)
        config_payload = {
            "executable": str(ai_core.executable),
            "config_file": str(ai_core.config_file),
            "parallel_instances": ai_core.parallel_instances,
        }
        request = ta_pb2.SystemModifyModelNodeConfigRequest(
            strModelNodeName=self.config.test.model_name,
            strConfig=json.dumps(config_payload),
            lTimeoutInSeconds=timeout_seconds,
        )
        self._call_rpc(
            self.system_stub.ModifyModelNodeConfig,
            request,
            "ModifyModelNodeConfig",
        )

    def load_model(self) -> None:
        """Load the requested detection model within PROVEtech:TA."""

        assert self.system_stub is not None
        model_name = self.config.test.model_name
        self.logger.info("Loading detection model '%s'", model_name)
        request = ta_pb2.SystemLoadModelRequest(strModelName=model_name)
        self._call_rpc(self.system_stub.LoadModel, request, "LoadModel")

    def start_measurement(self) -> None:
        """Start the measurement run to stream video and AI signals."""

        assert self.measure_stub is not None
        self.logger.info("Starting measurement run")
        request = ta_pb2.MeasureStartRequest(bSaveToDisk=False)
        self._call_rpc(self.measure_stub.Start, request, "MeasureStart")

    def wait_for_completion(self, max_duration: Optional[int], poll_interval: float) -> List[Dict[str, Any]]:
        """Monitor configured signals until the measurement stops."""

        assert self.measure_stub is not None and self.system_stub is not None
        signals = self.config.test.log_signals
        self.logger.info("Monitoring %d signals from AI-Core", len(signals))
        collected: List[Dict[str, Any]] = []
        start_time = time.time()

        while True:
            timestamp = datetime.now(timezone.utc).isoformat()
            row: Dict[str, Any] = {"timestamp": timestamp}
            for signal_name in signals:
                value = self._read_signal(signal_name)
                row[signal_name] = value
            collected.append(row)

            running = self._is_measurement_running()
            if not running:
                self.logger.info("Measurement reported as finished")
                break
            if max_duration and (time.time() - start_time) >= max_duration:
                self.logger.warning("Maximum monitoring duration reached (%ss)", max_duration)
                break
            time.sleep(poll_interval)
        return collected

    def stop_measurement(self) -> None:
        """Stop the measurement if it is still running."""

        assert self.measure_stub is not None
        self.logger.info("Stopping measurement")
        request = ta_pb2.MeasureStopRequest()
        self._call_rpc(self.measure_stub.Stop, request, "MeasureStop")

    def fetch_test_result(self) -> Dict[str, Any]:
        """Retrieve the overall test result from PROVEtech:TA."""

        assert self.system_stub is not None
        request = ta_pb2.SystemGetResultRequest()
        response = self._call_rpc(
            self.system_stub.GetResult,
            request,
            "GetResult",
        )
        result_value = getattr(response, "RetVal", None)
        additional = getattr(response, "piAdditionalResultValue", None)
        add_to_protocol = getattr(response, "pbAddResultToProtocol", None)
        return {
            "result": result_value,
            "additional_result": additional,
            "add_to_protocol": add_to_protocol,
        }

    def _is_measurement_running(self) -> bool:
        assert self.measure_stub is not None
        request = ta_pb2.MeasureIsRunningRequest()
        response = self._call_rpc(
            self.measure_stub.IsRunning,
            request,
            "MeasureIsRunning",
        )
        return bool(getattr(response, "RetVal", False))

    def _read_signal(self, signal_name: str) -> Any:
        assert self.system_stub is not None
        request = ta_pb2.SystemGetSignalRequest(
            strSignalName=signal_name,
            bInterpreted=True,
        )
        response = self._call_rpc(
            self.system_stub.GetSignal,
            request,
            f"GetSignal[{signal_name}]",
        )
        which = response.WhichOneof("RetVal")
        if not which:
            raise RuntimeError(f"Signal {signal_name} returned no value")
        return getattr(response, which)

    def _call_rpc(self, method, request, name: str):
        timeout_s = max(self.config.timeout_ms / 1000.0, 5)
        try:
            return method(request, timeout=timeout_s)
        except grpc.RpcError as exc:
            status = exc.code()
            if status == grpc.StatusCode.DEADLINE_EXCEEDED:
                self.logger.error("RPC %s timed out after %sms", name, self.config.timeout_ms)
                raise TimeoutError(f"RPC {name} timed out") from exc
            if status in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.UNIMPLEMENTED):
                self.logger.error("RPC %s failed: %s", name, exc.details())
                raise ConnectionError(f"RPC {name} failed: {exc.details()}") from exc
            self.logger.exception("Unexpected RPC error for %s", name)
            raise


def export_results(data: List[Dict[str, Any]], metadata: Dict[str, Any], output_dir: Path, logger) -> None:
    """Persist collected signal data to CSV and JSON outputs."""

    if not data:
        logger.warning("No signal data collected; skipping export")
        return
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(data)
    csv_path = output_dir / "signals.csv"
    json_path = output_dir / "result_summary.json"

    df.to_csv(csv_path, index=False)
    payload = {
        "metadata": metadata,
        "signals": data,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    logger.info("Results exported to %s and %s", csv_path, json_path)


def launch_ai_core(config: AutomationConfig, logger, skip_launch: bool) -> Optional[subprocess.Popen[bytes]]:
    """Launch AI-Core if requested."""

    if skip_launch:
        logger.info("Skipping AI-Core launch as requested")
        return None
    executable = config.ai_core.executable
    config_file = config.ai_core.config_file
    if not executable.exists():
        logger.warning("AI-Core executable not found at %s", executable)
        return None
    if not config_file.exists():
        logger.warning("AI-Core configuration file not found at %s", config_file)
    arguments = [str(config_file)] if config_file.exists() else []
    try:
        return start_process(executable, arguments, logger)
    except ProcessLaunchError as exc:
        logger.error("Failed to launch AI-Core: %s", exc)
        return None


def launch_provetech(config: AutomationConfig, logger, skip_launch: bool) -> Optional[subprocess.Popen[bytes]]:
    """Launch PROVEtech:TA in gRPC server mode."""

    if skip_launch:
        logger.info("Skipping PROVEtech:TA launch as requested")
        return None
    executable = config.test.ta_executable
    if not executable:
        logger.warning("No PROVEtech:TA executable configured; skipping launch")
        return None
    arguments = [f"--grpc-port={config.grpc.port}", "--automation"]
    try:
        return start_process(executable, arguments, logger)
    except ProcessLaunchError as exc:
        logger.error("Failed to launch PROVEtech:TA: %s", exc)
        raise


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_arguments(argv)
    config_path = Path(args.config) if args.config else Path(__file__).with_name("config.yaml")
    config = load_configuration(config_path)
    apply_cli_overrides(config, args)

    logger = setup_logging(config.logging.level, config.logging.file)
    update_log_level(logger, args.log_level)

    ai_core_process = None
    ta_process = None

    try:
        ta_process = launch_provetech(config, logger, args.skip_ta_launch)
        if ta_process is not None:
            # Allow server to initialise before attempting to connect.
            logger.info("Waiting for PROVEtech:TA to initialise")
            time.sleep(5)

        controller = TestAutomationController(config, logger)
        controller.connect()

        ai_core_process = launch_ai_core(config, logger, args.skip_ai_core)

        controller.configure_video()
        controller.configure_ai_core()
        controller.load_model()
        controller.start_measurement()
        signal_data = controller.wait_for_completion(
            max_duration=args.monitor_seconds,
            poll_interval=args.poll_interval,
        )
        controller.stop_measurement()
        test_result = controller.fetch_test_result()

        export_results(signal_data, test_result, config.test.output_dir, logger)
        logger.info("Automation workflow completed successfully")
        return 0
    except (ConfigurationError, ConnectionError, TimeoutError, ProcessLaunchError) as exc:
        logger.error("Automation failed: %s", exc)
        return 1
    except KeyboardInterrupt:
        logger.warning("Automation interrupted by user")
        return 2
    finally:
        if ai_core_process is not None:
            _terminate_process(ai_core_process, logger)
        if ta_process is not None:
            _terminate_process(ta_process, logger)
        if controller := locals().get("controller"):
            channel = getattr(controller, "channel", None)
            if channel is not None:
                channel.close()


if __name__ == "__main__":
    sys.exit(main())
