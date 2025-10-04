# AutomatedAITest

AutomatedAITest is a Python-based orchestration tool that automates end-to-end
AI-assisted verification workflows for PROVEtech:TA 2025 SE coupled with
AI-Core 2025 SE. The application launches the toolchain, configures video
routing, links AI-Core projects, executes the requested detection model, and
collects KPI signals and results for offline analysis.

## Key Features

- Launch PROVEtech:TA in gRPC automation mode with a custom port.
- Configure AI-Core executable, project configuration, and timeout settings.
- Set up video routing (device, driver, resolution) for AI-Core ingestion.
- Start detection models and monitor live AI-Core signals.
- Export captured signals to CSV and JSON artefacts under the configured
  results directory.
- Robust logging with timestamps and CLI overrides for mission-critical
  parameters.

## Prerequisites

- Windows 10/11 x64 host with Python 3.9 or newer.
- PROVEtech:TA 2025 SE and AI-Core 2025 SE installed locally.
- The `testautomation.proto` file provided with PROVEtech:TA (already included
  in this repository).

## Installation

1. Clone the repository and open a PowerShell terminal in the project root.
2. Create and activate a Python virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the required dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Generating gRPC Stubs

The repository already contains `testautomation_pb2.py` and
`testautomation_pb2_grpc.py`. If PROVEtech releases an updated
`testautomation.proto`, regenerate the stubs using:

```powershell
python -m grpc_tools.protoc `
    -I . `
    --python_out=. `
    --grpc_python_out=. `
    testautomation.proto
```

> **Tip:** When working from another directory, adjust the `-I` include path to
> point at the folder containing `testautomation.proto`.

## Configuration

All configuration values live in `config.yaml`. Out-of-the-box defaults cover a
single AI-Core instance ingesting video from `FrontCam`. See
[CONFIGURATION.md](CONFIGURATION.md) for a detailed breakdown of all
parameters. Key sections include:

- `grpc`: Hostname and port for PROVEtech:TA's automation server.
- `ai_core`: Executable path, project configuration, timeout, and instance
  count.
- `video`: Camera name, driver identifier, and resolution to stream.
- `test`: Detection model name, PROVEtech:TA executable path, result folder,
  and monitored signal list.
- `logging`: Log level and output file path.

## Running the Automation

Execute the automation script from the project root (virtual environment
activated):

```powershell
python automate_test.py
```

### CLI Overrides

Use CLI parameters to override YAML values for ad-hoc runs. Examples:

```powershell
# Override model name and timeout
python automate_test.py --model VisionNet --timeout 15000

# Change video source and send results to a different folder
python automate_test.py `
    --video-source RearCam `
    --video-driver PCIeCapture0 `
    --resolution 1280x720 `
    --output-dir D:/PROVEtechRuns/2025-05-22

# Point to an alternative configuration file and skip launching PROVEtech:TA
python automate_test.py --config C:/Configs/nightly.yaml --skip-ta-launch
```

Refer to `python automate_test.py --help` for the full list of switches,
including `--ai-core-config`, `--ai-core-executable`, `--log-signal`, and
`--monitor-seconds`.

## Result Artefacts

Upon completion the script writes:

- `signals.csv`: Timestamped table of monitored signals.
- `result_summary.json`: Metadata summary containing the PROVEtech:TA result
  status and the captured samples.

Both files are stored in the directory configured via `test.output_dir` (default
`./results`). Load the CSV into Excel, pandas, or BI tools to analyse AI-Core
KPIs across the test duration.

## Troubleshooting

| Issue | Recommendation |
| ----- | -------------- |
| gRPC connection fails | Ensure PROVEtech:TA was launched with automation mode enabled and that the gRPC port is not blocked by Windows Firewall. Use `--grpc-host`/`--grpc-port` overrides if the defaults changed. |
| AI-Core executable not found | Update `ai_core.executable` in `config.yaml` or use `--ai-core-executable`. Confirm that the `.cfg` file path is valid. |
| Signal returns empty values | Verify that the signal names under `test.log_signals` exist in PROVEtech:TA. Use the GUI to inspect available signals or adjust interpretation mode if raw values are needed. |
| Timeout exceptions | Increase `ai_core.timeout_ms` in `config.yaml` or `--timeout` when dealing with high start-up latencies. |
| Results folder missing | The script automatically creates missing directories. Ensure the executing user has write permissions for the configured output directory. |

## Support

- Review [CONFIGURATION.md](CONFIGURATION.md) for advanced parameter tuning,
  TLS considerations, and multi-instance setups.
- Enable verbose logging with `--log-level DEBUG` and attach the generated log
  file when escalating issues to the PROVEtech support team.
