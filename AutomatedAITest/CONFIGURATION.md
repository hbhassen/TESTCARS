# Configuration Guide

This document describes every configurable aspect of the AutomatedAITest
application. Use it to tailor the automation workflow to specific laboratory
setups, multi-instance executions, and deployment security requirements.

## File Overview

- `config.yaml` &mdash; Primary configuration file consumed by `automate_test.py`.
- CLI flags &mdash; All critical parameters can be overridden at runtime without
  editing YAML.

## YAML Structure

```yaml
grpc:
  host: localhost
  port: 50051
ai_core:
  executable: "C:/Program Files/AICORE/AICORE.exe"
  config_file: "C:/AIcoreProjects/DetectMode/detectmode.cfg"
  timeout_ms: 10000
  parallel_instances: 1
video:
  device_name: "FrontCam"
  driver_id: "IntegratedCamera0"
  resolution: "1920x1080"
test:
  model_name: "DetectModeModel"
  ta_executable: "C:/Program Files/PROVEtech/PROVEtechTA.exe"
  output_dir: "./results"
  log_signals:
    - "IconDetection.Result"
    - "IconDetection.Score"
logging:
  level: "INFO"
  file: "./logs/automation.log"
```

### grpc

| Key  | Default    | Description |
| ---- | ---------- | ----------- |
| `host` | `localhost` | Hostname or IP where PROVEtech:TA exposes its gRPC Test Automation API. Use the Windows machine name or loopback when running locally. |
| `port` | `50051` | TCP port for the gRPC server. Match the value provided when launching PROVEtech:TA with automation enabled. Override with `--grpc-port`. |

### ai_core

| Key | Default | Description |
| --- | ------- | ----------- |
| `executable` | `C:/Program Files/AICORE/AICORE.exe` | Path to the AI-Core 2025 SE executable. Override with `--ai-core-executable`. |
| `config_file` | `C:/AIcoreProjects/DetectMode/detectmode.cfg` | AI-Core project configuration to load. Override with `--ai-core-config`. |
| `timeout_ms` | `10000` | Timeout for AI-Core related RPCs (model configuration, linking). Override with `--timeout`. |
| `parallel_instances` | `1` | Number of AI-Core instances to spawn for multi-camera / multi-model tests. Reflects how many times the configuration is applied internally. |

### video

| Key | Default | Description |
| --- | ------- | ----------- |
| `device_name` | `FrontCam` | Logical PROVEtech:TA video source name. Override with `--video-source`. |
| `driver_id` | `IntegratedCamera0` | Driver identifier used by PROVEtech:TA to bind the device. Override with `--video-driver`. |
| `resolution` | `1920x1080` | Capture resolution (WidthxHeight). Override with `--resolution`. |

### test

| Key | Default | Description |
| --- | ------- | ----------- |
| `model_name` | `DetectModeModel` | Detection model node to load inside PROVEtech:TA. Override with `--model`. |
| `ta_executable` | `C:/Program Files/PROVEtech/PROVEtechTA.exe` | Executable path for launching PROVEtech:TA. Override with `--ta-executable`. |
| `output_dir` | `./results` | Directory where CSV/JSON artefacts are stored. Override with `--output-dir`. |
| `log_signals` | `IconDetection.Result`, `IconDetection.Score` | AI-Core signal names to monitor. Use repeated `--log-signal` flags to override the list from CLI. |

### logging

| Key | Default | Description |
| --- | ------- | ----------- |
| `level` | `INFO` | Application log level. Override with `--log-level`. |
| `file` | `./logs/automation.log` | Absolute or relative path of the log file. Parent directories are created automatically. |

## CLI Overrides

All keys above can be overridden on demand. Example combinations:

```powershell
# Run with an alternative AI-Core project and additional signal capture
python automate_test.py `
    --ai-core-config D:/AICore/parking.cfg `
    --model ParkingAssist `
    --log-signal IconDetection.Result `
    --log-signal ParkingAssist.Status

# Temporarily switch to a remote PROVEtech:TA instance
python automate_test.py --grpc-host 10.10.1.20 --grpc-port 51000
```

## Advanced Scenarios

### Switching Models Dynamically

To execute multiple models without editing YAML:

1. Provide the first model via `--model ModelA` and run the automation.
2. Launch the next run with `--model ModelB --ai-core-config C:/Projects/modelB.cfg`.
3. Optionally change the monitored signals via repeated `--log-signal` flags.

The script reloads the model and updates AI-Core linkage on each invocation.

### Multiple AI-Core Instances

Set `ai_core.parallel_instances` to the number of AI-Core runtimes required.
Ensure that `config_file` references a configuration capable of handling
multiple pipelines. When running from CLI:

```powershell
python automate_test.py --timeout 20000 --log-level DEBUG
```

Increase the timeout because launching several AI-Core instances prolongs the
initial handshake. The script passes `parallel_instances` to the configuration
payload shared with PROVEtech:TA.

### Adjusting Connection Timeouts

High-latency network paths or slow system start-up sequences may necessitate a
higher timeout. Update `ai_core.timeout_ms` or run with `--timeout 30000` to
propagate the value to all RPC invocations (`LoadModel`, `ModifyModelNodeConfig`,
etc.).

### Changing Video Source

Use `--video-source` and `--video-driver` to point at a different camera without
modifying YAML. If resolution differs per sensor, append `--resolution 1280x720`
(or another valid format). The script applies the changes via
`SystemModifyVideoAudioConfig` before starting the measurement.

## Security Considerations (gRPC over TLS)

- PROVEtech:TA supports TLS-enabled gRPC endpoints starting from 2025 SE. Update
  the automation script to use `grpc.secure_channel` with server certificates if
  transmitting over untrusted networks.
- Store certificates securely and avoid hard-coding secrets into `config.yaml`.
- Restrict Windows Firewall rules to limit access to the gRPC port.

## Folder Structure

Recommended structure for reproducible test campaigns:

```
AutomatedAITest/
├── logs/                # Rolling automation logs per execution
├── results/             # Exported CSV/JSON artefacts
├── models/              # AI-Core project files (.cfg)
└── recordings/          # Optional raw video captures for offline review
```

Update `config.yaml` paths to point at the appropriate folders. The automation
script creates `logs/` and `results/` automatically when missing.

## Example CSV Output

```
timestamp,IconDetection.Result,IconDetection.Score
2025-05-20T08:42:11.254000+00:00,1,0.982
2025-05-20T08:42:11.754000+00:00,1,0.978
2025-05-20T08:42:12.254000+00:00,0,0.412
```

Each row represents a polling cycle. `timestamp` is in ISO 8601 with UTC
timezone, and the signal columns reflect interpreted values retrieved from
`SystemGetSignal`. Import this CSV into analytics tools to compute detection
rates, latency, or KPI distributions.

