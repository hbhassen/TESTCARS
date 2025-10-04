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
  mode: "device"
  device_name: "FrontCam"
  driver_id: "IntegratedCamera0"
  resolution: "1920x1080"
  # file_path: "D:/Recordings/frontcam.mp4"
  # webcam_index: 0
  loop_file: false
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
| `mode` | `device` | Ingestion mode: `device` keeps the legacy capture card routing, `webcam` uses the local PC webcam, and `file` replays a recorded video. Override with `--video-mode`. |
| `device_name` | `FrontCam` | Logical PROVEtech:TA video source name. Override with `--video-source`. |
| `driver_id` | `IntegratedCamera0` | Driver identifier used by PROVEtech:TA to bind the device. Override with `--video-driver`. |
| `resolution` | `1920x1080` | Capture resolution (WidthxHeight). Override with `--resolution`. |
| `file_path` | _unset_ | Absolute or relative path to the recorded footage when `mode` is `file`. Override with `--video-file`. |
| `webcam_index` | _unset_ | Numeric index of the Windows webcam to bind when `mode` is `webcam`. Override with `--webcam-index`. |
| `loop_file` | `false` | Loop recorded footage instead of stopping at the end. Toggle via `--loop-video` / `--no-loop-video`. |

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

To temporarily stream from the PC webcam or replay a file without editing the
YAML:

```powershell
# Webcam capture
python automate_test.py --video-mode webcam --webcam-index 0

# Recorded footage on loop
python automate_test.py --video-mode file --video-file D:/Recordings/drive.mp4 --loop-video
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

Select the ingestion mode with `video.mode` (or `--video-mode`).

- `device` — Default capture card / hardware input workflow. Combine with
  `--video-source`, `--video-driver`, and `--resolution` to target the desired
  channel.
- `webcam` — Streams directly from the Windows webcam stack. Provide the index
  with `video.webcam_index` or `--webcam-index 0`. The script preserves legacy
  overrides such as `--video-source` when the logical name in PROVEtech:TA must
  remain stable.
- `file` — Replays recorded footage from disk. Supply the path through
  `video.file_path` or `--video-file D:/Recordings/run01.mp4` and optionally
  loop playback using `video.loop_file` / `--loop-video`.

When switching modes, the automation repackages the video configuration payload
accordingly before invoking `SystemModifyVideoAudioConfig`.

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


---

# Guide de configuration (français)

Ce document détaille chaque paramètre configurable de l'application AutomatedAITest. Utilisez-le pour adapter le flux d'automatisation aux laboratoires spécifiques, aux exécutions multi-instances et aux exigences de sécurité.

## Vue d'ensemble des fichiers

- `config.yaml` — Fichier de configuration principal consommé par `automate_test.py`.
- Options CLI — Tous les paramètres critiques peuvent être surchargés à l'exécution sans modifier le YAML.

## Structure YAML

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
  mode: "device"
  device_name: "FrontCam"
  driver_id: "IntegratedCamera0"
  resolution: "1920x1080"
  # file_path: "D:/Recordings/frontcam.mp4"
  # webcam_index: 0
  loop_file: false
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

| Clé | Valeur par défaut | Description |
| --- | ----------------- | ----------- |
| `host` | `localhost` | Nom d'hôte ou IP où PROVEtech:TA expose son API gRPC. Utilisez le nom de la machine Windows ou la boucle locale pour un usage local. |
| `port` | `50051` | Port TCP du serveur gRPC. Doit correspondre à la valeur fournie lors du lancement de PROVEtech:TA en mode automatisation. Surcharge possible avec `--grpc-port`. |

### ai_core

| Clé | Valeur par défaut | Description |
| --- | ----------------- | ----------- |
| `executable` | `C:/Program Files/AICORE/AICORE.exe` | Chemin vers l'exécutable AI-Core 2025 SE. Surcharge avec `--ai-core-executable`. |
| `config_file` | `C:/AIcoreProjects/DetectMode/detectmode.cfg` | Fichier de configuration du projet AI-Core. Surcharge avec `--ai-core-config`. |
| `timeout_ms` | `10000` | Temporisation pour les RPC liés à AI-Core (chargement de modèle, liaison). Surcharge avec `--timeout`. |
| `parallel_instances` | `1` | Nombre d'instances AI-Core à lancer pour les tests multi-caméras / multi-modèles. |

### video

| Clé | Valeur par défaut | Description |
| --- | ----------------- | ----------- |
| `mode` | `device` | Mode d'ingestion : `device` conserve la capture matérielle, `webcam` utilise la webcam locale et `file` rejoue une vidéo enregistrée. Surcharge avec `--video-mode`. |
| `device_name` | `FrontCam` | Nom logique de la source vidéo PROVEtech:TA. Surcharge avec `--video-source`. |
| `driver_id` | `IntegratedCamera0` | Identifiant du pilote utilisé par PROVEtech:TA pour lier le périphérique. Surcharge avec `--video-driver`. |
| `resolution` | `1920x1080` | Résolution de capture (Largeur x Hauteur). Surcharge avec `--resolution`. |
| `file_path` | _non défini_ | Chemin absolu ou relatif de la vidéo enregistrée lorsque `mode` vaut `file`. Surcharge avec `--video-file`. |
| `webcam_index` | _non défini_ | Index numérique de la webcam Windows à utiliser lorsque `mode` vaut `webcam`. Surcharge avec `--webcam-index`. |
| `loop_file` | `false` | Boucler la lecture de la vidéo enregistrée au lieu de s'arrêter en fin de fichier. Activable via `--loop-video` / `--no-loop-video`. |

### test

| Clé | Valeur par défaut | Description |
| --- | ----------------- | ----------- |
| `model_name` | `DetectModeModel` | Nom du modèle de détection à charger dans PROVEtech:TA. Surcharge avec `--model`. |
| `ta_executable` | `C:/Program Files/PROVEtech/PROVEtechTA.exe` | Chemin de l'exécutable PROVEtech:TA. Surcharge avec `--ta-executable`. |
| `output_dir` | `./results` | Répertoire de stockage des artefacts CSV/JSON. Surcharge avec `--output-dir`. |
| `log_signals` | `IconDetection.Result`, `IconDetection.Score` | Noms des signaux AI-Core à surveiller. Utilisez `--log-signal` plusieurs fois pour définir une nouvelle liste. |

### logging

| Clé | Valeur par défaut | Description |
| --- | ----------------- | ----------- |
| `level` | `INFO` | Niveau de journalisation de l'application. Surcharge avec `--log-level`. |
| `file` | `./logs/automation.log` | Chemin absolu ou relatif du fichier de log. Les dossiers parents sont créés automatiquement. |

## Surcharges CLI

Tous les paramètres ci-dessus peuvent être ajustés à la volée. Exemples :

```powershell
# Utiliser un projet AI-Core alternatif et capturer des signaux supplémentaires
python automate_test.py `
    --ai-core-config D:/AICore/parking.cfg `
    --model ParkingAssist `
    --log-signal IconDetection.Result `
    --log-signal ParkingAssist.Status

# Basculer temporairement vers une instance PROVEtech:TA distante
python automate_test.py --grpc-host 10.10.1.20 --grpc-port 51000
```

Pour exploiter temporairement la webcam ou rejouer un fichier sans modifier le YAML :

```powershell
# Capture webcam
python automate_test.py --video-mode webcam --webcam-index 0

# Lecture d'une vidéo enregistrée en boucle
python automate_test.py --video-mode file --video-file D:/Recordings/drive.mp4 --loop-video
```

## Scénarios avancés

### Changement dynamique de modèles

Pour exécuter plusieurs modèles sans modifier le YAML :

1. Lancez une première exécution avec `--model ModelA`.
2. Rejouez avec `--model ModelB --ai-core-config C:/Projects/modelB.cfg`.
3. Ajustez au besoin la liste des signaux via `--log-signal`.

Le script recharge le modèle et met à jour la liaison AI-Core à chaque invocation.

### Instances AI-Core multiples

Définissez `ai_core.parallel_instances` au nombre d'exécutions AI-Core nécessaires. Assurez-vous que `config_file` supporte plusieurs pipelines. Exemple en CLI :

```powershell
python automate_test.py --timeout 20000 --log-level DEBUG
```

Augmentez la temporisation car plusieurs instances prolongent la phase d'initialisation. Le script transmet `parallel_instances` à la configuration envoyée à PROVEtech:TA.

### Ajustement des temporisations

Les réseaux lents ou les démarrages prolongés nécessitent parfois une temporisation plus élevée. Mettez à jour `ai_core.timeout_ms` ou lancez avec `--timeout 30000` pour propager la valeur à toutes les RPC (`LoadModel`, `ModifyModelNodeConfig`, etc.).

### Modification de la source vidéo

Sélectionnez le mode d'ingestion via `video.mode` (ou `--video-mode`).

- `device` — Flux historique depuis une carte de capture ou un driver dédié. Combinez avec `--video-source`, `--video-driver` et `--resolution` pour cibler le canal souhaité.
- `webcam` — Diffuse directement via la pile webcam de Windows. Fournissez l'index avec `video.webcam_index` ou `--webcam-index 0`. Le nom logique (`--video-source`) reste disponible pour conserver la nomenclature PROVEtech:TA.
- `file` — Rejoue une vidéo enregistrée depuis le disque. Indiquez le chemin via `video.file_path` ou `--video-file D:/Recordings/run01.mp4` et bouclez la lecture avec `video.loop_file` / `--loop-video` si nécessaire.

Lors du changement de mode, l'automatisation adapte automatiquement la charge utile envoyée à `SystemModifyVideoAudioConfig`.

## Considérations de sécurité (gRPC via TLS)

- PROVEtech:TA prend en charge les points de terminaison gRPC sécurisés (TLS) à partir de la version 2025 SE. Adaptez le script pour utiliser `grpc.secure_channel` avec les certificats serveur lors de transmissions sur réseau non fiable.
- Stockez les certificats en toute sécurité et évitez de coder en dur des secrets dans `config.yaml`.
- Restreignez les règles du pare-feu Windows pour limiter l'accès au port gRPC.

## Structure de dossiers recommandée

```text
AutomatedAITest/
├── logs/                # Journaux d'automatisation par exécution
├── results/             # Artefacts CSV/JSON exportés
├── models/              # Fichiers de projets AI-Core (.cfg)
└── recordings/          # Éventuelles captures vidéo pour analyse hors ligne
```

Mettez à jour les chemins de `config.yaml` vers les dossiers appropriés. Le script crée automatiquement `logs/` et `results/` s'ils n'existent pas.

## Exemple de sortie CSV

```text
timestamp,IconDetection.Result,IconDetection.Score
2025-05-20T08:42:11.254000+00:00,1,0.982
2025-05-20T08:42:11.754000+00:00,1,0.978
2025-05-20T08:42:12.254000+00:00,0,0.412
```

Chaque ligne correspond à un cycle d'interrogation. `timestamp` est horodaté ISO 8601 en UTC, et les colonnes de signaux reflètent les valeurs interprétées renvoyées par `SystemGetSignal`. Importez ce CSV dans vos outils analytiques pour calculer les taux de détection, la latence ou d'autres KPI.
