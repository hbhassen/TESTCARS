# AutomatedAITest (Version française)

## Présentation du projet

AutomatedAITest est un outil d'orchestration écrit en Python qui automatise de bout en bout les campagnes de vérification assistées par l'IA pour PROVEtech:TA 2025 SE couplé à AI-Core 2025 SE. L'application démarre la chaîne d'outils, configure l'acheminement vidéo, lie les projets AI-Core, exécute le modèle de détection demandé et collecte les signaux KPI ainsi que les résultats pour l'analyse hors ligne.

## Fonctionnalités clés

- Lancement de PROVEtech:TA en mode automatisation gRPC avec port personnalisé.
- Configuration de l'exécutable AI-Core, du projet et des paramètres de temporisation.
- Mise en place de l'acheminement vidéo (périphérique, pilote, résolution) pour l'ingestion AI-Core.
- Démarrage des modèles de détection et surveillance des signaux AI-Core en direct.
- Export des signaux capturés vers des artefacts CSV et JSON dans le répertoire de résultats configuré.
- Journalisation robuste avec horodatages et paramètres critiques surchargés en ligne de commande.

## Prérequis

- Hôte Windows 10/11 x64 avec Python 3.9 ou version ultérieure.
- PROVEtech:TA 2025 SE et AI-Core 2025 SE installés localement.
- Fichier `testautomation.proto` fourni avec PROVEtech:TA (déjà inclus dans ce dépôt).

## Installation

1. Cloner le dépôt et ouvrir une console PowerShell dans la racine du projet.
2. Créer et activer un environnement virtuel Python :

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Installer les dépendances requises :

   ```powershell
   pip install -r requirements.txt
   ```

## Génération des stubs gRPC

Le dépôt contient déjà `testautomation_pb2.py` et `testautomation_pb2_grpc.py`. Si PROVEtech publie une nouvelle version de `testautomation.proto`, régénérez les stubs avec :

```powershell
python -m grpc_tools.protoc `
    -I . `
    --python_out=. `
    --grpc_python_out=. `
    testautomation.proto
```

> **Astuce :** si vous travaillez depuis un autre dossier, ajustez l'option `-I` pour pointer vers le dossier qui contient `testautomation.proto`.

## Configuration

Toutes les valeurs de configuration se trouvent dans `config.yaml`. Les valeurs par défaut couvrent une instance unique d'AI-Core ingérant la vidéo `FrontCam`. Consultez [CONFIGURATION.fr.md](CONFIGURATION.fr.md) pour une description détaillée de chaque paramètre. Les sections principales comprennent :

- `grpc` : nom d'hôte et port du serveur d'automatisation PROVEtech:TA.
- `ai_core` : chemin de l'exécutable, fichier de configuration projet, temporisation et nombre d'instances.
- `video` : nom de caméra, identifiant de pilote et résolution à diffuser.
- `test` : nom du modèle de détection, chemin de PROVEtech:TA, dossier de résultats et liste de signaux surveillés.
- `logging` : niveau de journalisation et chemin du fichier de log.

## Exécution de l'automatisation

Exécutez le script d'automatisation depuis la racine du projet (environnement virtuel activé) :

```powershell
python automate_test.py
```

### Surcharges CLI

Utilisez les paramètres CLI pour remplacer à la volée les valeurs du YAML. Exemples :

```powershell
# Remplacer le nom du modèle et la temporisation
python automate_test.py --model VisionNet --timeout 15000

# Modifier la source vidéo et envoyer les résultats dans un autre dossier
python automate_test.py `
    --video-source RearCam `
    --video-driver PCIeCapture0 `
    --resolution 1280x720 `
    --output-dir D:/PROVEtechRuns/2025-05-22

# Pointer vers un fichier de configuration alternatif et éviter le lancement de PROVEtech:TA
python automate_test.py --config C:/Configs/nightly.yaml --skip-ta-launch
```

Consultez `python automate_test.py --help` pour la liste complète des options, notamment `--ai-core-config`, `--ai-core-executable`, `--log-signal` et `--monitor-seconds`.

## Artefacts de résultats

À la fin de l'exécution, le script génère :

- `signals.csv` : tableau horodaté des signaux surveillés.
- `result_summary.json` : résumé contenant l'état du résultat PROVEtech:TA et les échantillons capturés.

Les deux fichiers sont enregistrés dans le répertoire défini par `test.output_dir` (par défaut `./results`). Chargez le CSV dans Excel, pandas ou un outil BI pour analyser les KPI AI-Core sur la durée du test.

## Dépannage

| Problème | Recommandation |
| -------- | --------------- |
| Échec de connexion gRPC | Vérifiez que PROVEtech:TA est lancé en mode automatisation et que le port gRPC n'est pas bloqué par le pare-feu Windows. Utilisez `--grpc-host` / `--grpc-port` si les valeurs par défaut ont changé. |
| Exécutable AI-Core introuvable | Mettez à jour `ai_core.executable` dans `config.yaml` ou utilisez `--ai-core-executable`. Vérifiez que le chemin du fichier `.cfg` est valide. |
| Signaux vides | Confirmez que les noms de signaux sous `test.log_signals` existent dans PROVEtech:TA. Utilisez l'interface graphique pour inspecter les signaux disponibles ou ajustez le mode d'interprétation si nécessaire. |
| Exceptions de temporisation | Augmentez `ai_core.timeout_ms` dans `config.yaml` ou `--timeout` pour les phases de démarrage plus longues. |
| Dossier de résultats manquant | Le script crée automatiquement les dossiers manquants. Assurez-vous que l'utilisateur possède les droits d'écriture sur le répertoire configuré. |

## Support

- Consultez [CONFIGURATION.fr.md](CONFIGURATION.fr.md) pour les réglages avancés, les considérations TLS et les configurations multi-instances.
- Activez la journalisation détaillée avec `--log-level DEBUG` et joignez le fichier de log généré lors des escalades vers l'équipe support PROVEtech.
