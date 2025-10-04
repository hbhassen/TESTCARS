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

| Clé | Valeur par défaut | Description |
| --- | ----------------- | ----------- |
| `host` | `localhost` | Nom d'hôte ou IP où PROVEtech:TA expose son API gRPC de Test Automation. Utilisez le nom de la machine Windows ou la boucle locale pour un usage local. |
| `port` | `50051` | Port TCP du serveur gRPC. Doit correspondre à la valeur fournie lors du lancement de PROVEtech:TA avec l'automatisation activée. Remplaçable avec `--grpc-port`. |

### ai_core

| Clé | Valeur par défaut | Description |
| --- | ----------------- | ----------- |
| `executable` | `C:/Program Files/AICORE/AICORE.exe` | Chemin de l'exécutable AI-Core 2025 SE. Remplaçable avec `--ai-core-executable`. |
| `config_file` | `C:/AIcoreProjects/DetectMode/detectmode.cfg` | Configuration du projet AI-Core à charger. Remplaçable avec `--ai-core-config`. |
| `timeout_ms` | `10000` | Temporisation des RPC liés à AI-Core (configuration de modèle, liaison). Remplaçable avec `--timeout`. |
| `parallel_instances` | `1` | Nombre d'instances AI-Core à lancer pour les tests multi-caméras / multi-modèles. Définit combien de fois la configuration est appliquée en interne. |

### video

| Clé | Valeur par défaut | Description |
| --- | ----------------- | ----------- |
| `device_name` | `FrontCam` | Nom logique de la source vidéo dans PROVEtech:TA. Remplaçable avec `--video-source`. |
| `driver_id` | `IntegratedCamera0` | Identifiant du pilote utilisé par PROVEtech:TA pour lier le périphérique. Remplaçable avec `--video-driver`. |
| `resolution` | `1920x1080` | Résolution de capture (Largeur x Hauteur). Remplaçable avec `--resolution`. |

### test

| Clé | Valeur par défaut | Description |
| --- | ----------------- | ----------- |
| `model_name` | `DetectModeModel` | Nœud de modèle de détection à charger dans PROVEtech:TA. Remplaçable avec `--model`. |
| `ta_executable` | `C:/Program Files/PROVEtech/PROVEtechTA.exe` | Chemin de l'exécutable PROVEtech:TA. Remplaçable avec `--ta-executable`. |
| `output_dir` | `./results` | Dossier où les artefacts CSV/JSON sont stockés. Remplaçable avec `--output-dir`. |
| `log_signals` | `IconDetection.Result`, `IconDetection.Score` | Noms des signaux AI-Core à surveiller. Utilisez plusieurs options `--log-signal` pour remplacer la liste via la CLI. |

### logging

| Clé | Valeur par défaut | Description |
| --- | ----------------- | ----------- |
| `level` | `INFO` | Niveau de journalisation de l'application. Remplaçable avec `--log-level`. |
| `file` | `./logs/automation.log` | Chemin absolu ou relatif du fichier de log. Les dossiers parents sont créés automatiquement. |

## Surcharges CLI

Toutes les clés ci-dessus peuvent être surchargées à la demande. Exemples :

```powershell
# Exécuter avec un projet AI-Core alternatif et capturer des signaux supplémentaires
python automate_test.py `
    --ai-core-config D:/AICore/parking.cfg `
    --model ParkingAssist `
    --log-signal IconDetection.Result `
    --log-signal ParkingAssist.Status

# Basculement temporaire vers une instance PROVEtech:TA distante
python automate_test.py --grpc-host 10.10.1.20 --grpc-port 51000
```

## Scénarios avancés

### Commutation dynamique de modèles

Pour exécuter plusieurs modèles sans modifier le YAML :

1. Lancer la première exécution avec `--model ModelA`.
2. Relancer avec `--model ModelB --ai-core-config C:/Projects/modelB.cfg`.
3. Optionnellement, modifier les signaux surveillés via des options `--log-signal` répétées.

Le script recharge le modèle et met à jour la liaison AI-Core à chaque exécution.

### Instances AI-Core multiples

Définissez `ai_core.parallel_instances` sur le nombre d'exécutions AI-Core nécessaires. Assurez-vous que `config_file` référence une configuration capable de gérer plusieurs pipelines. Depuis la CLI :

```powershell
python automate_test.py --timeout 20000 --log-level DEBUG
```

Augmentez la temporisation, car le lancement de plusieurs instances AI-Core rallonge la phase d'initialisation. Le script transmet `parallel_instances` dans la charge de configuration envoyée à PROVEtech:TA.

### Ajustement des temporisations de connexion

Des chemins réseau à forte latence ou des séquences de démarrage lentes peuvent nécessiter une temporisation plus élevée. Mettez à jour `ai_core.timeout_ms` ou exécutez `--timeout 30000` pour appliquer la valeur à tous les RPC (`LoadModel`, `ModifyModelNodeConfig`, etc.).

### Changement de source vidéo

Utilisez `--video-source` et `--video-driver` pour sélectionner une autre caméra sans modifier le YAML. Si la résolution diffère selon le capteur, ajoutez `--resolution 1280x720` (ou un autre format valide). Le script applique les changements via `SystemModifyVideoAudioConfig` avant de démarrer la mesure.

## Considérations de sécurité (gRPC sur TLS)

- PROVEtech:TA prend en charge les points de terminaison gRPC sécurisés par TLS à partir de la version 2025 SE. Mettez à jour le script d'automatisation pour utiliser `grpc.secure_channel` avec des certificats serveur lors de transmissions sur des réseaux non fiables.
- Stockez les certificats en toute sécurité et évitez de coder en dur des secrets dans `config.yaml`.
- Restreignez les règles du pare-feu Windows pour limiter l'accès au port gRPC.

## Structure des dossiers

Structure recommandée pour des campagnes de test reproductibles :

```
AutomatedAITest/
├── logs/                # Journaux d'automatisation par exécution
├── results/             # Artefacts CSV/JSON exportés
├── models/              # Fichiers de projet AI-Core (.cfg)
└── recordings/          # Captures vidéo brutes optionnelles pour revue hors ligne
```

Mettez à jour les chemins `config.yaml` pour pointer vers les dossiers appropriés. Le script crée automatiquement `logs/` et `results/` s'ils sont absents.

## Exemple de sortie CSV

```
timestamp,IconDetection.Result,IconDetection.Score
2025-05-20T08:42:11.254000+00:00,1,0.982
2025-05-20T08:42:11.754000+00:00,1,0.978
2025-05-20T08:42:12.254000+00:00,0,0.412
```

Chaque ligne représente un cycle d'interrogation. `timestamp` est au format ISO 8601 en UTC et les colonnes de signaux reflètent les valeurs interprétées récupérées via `SystemGetSignal`. Importez ce CSV dans des outils d'analyse pour calculer les taux de détection, la latence ou la distribution des KPI.
