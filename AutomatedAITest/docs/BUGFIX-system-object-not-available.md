# Correctif : erreur « System object not available » lors de la configuration vidéo

## Résumé
- Date : 2025-10-06
- Auteur : Automatisation IA (support)
- Version du script : `automate_test.py` (commit courant)

## Symptômes
- Le journal affiche `Unexpected RPC error for ModifyVideoAudioConfig`.
- Le détail gRPC contient `"System" object not available`.
- L'exécution s'arrête avant l'activation de la mesure vidéo.

## Analyse de la cause racine
- PROVEtech:TA exige que l'appel `SystemModifyVideoAudioConfig` référence un objet vidéo déjà présent côté serveur.
- Lorsque `video.device_name` (ou `driver_id`) est vide dans `config.yaml`, le script envoyait un identifiant vide ou arbitraire (par exemple le nom du fichier vidéo).
- Aucun objet PROVEtech:TA ne correspondait à cet identifiant, d'où l'erreur « System object not available ».

## Correctif apporté
1. Génération d'une liste de candidats ordonnés (`device_name`, `driver_id`, nom de fichier, noms par défaut PROVEtech comme `FrontCam`).
2. Tentatives successives de configuration avec chaque candidat, en ignorant explicitement les erreurs `System object not available` jusqu'à trouver un nom valide.
3. Conservation du nom retenu pour l'activation de la mesure (`MeasureSetVideoAudio`).
4. Facteur commun de gestion des erreurs gRPC afin de réutiliser la logique en dehors du chemin nominal.

## Conseils de configuration
- **Recommandé :** Renseigner `video.device_name` dans `config.yaml` avec le nom exact du flux vidéo tel qu'il apparaît dans PROVEtech:TA.
- Si plusieurs sources existent, spécifier également `video.driver_id` pour limiter la recherche.
- En mode `file`, vérifier que `video.file_path` pointe vers un fichier accessible depuis la machine Windows qui exécute PROVEtech:TA.

## Validation
- Lancer le script avec la configuration problématique.
- Observer dans le journal la tentative sur plusieurs candidats puis la confirmation :
  ```
  Configuring video source FrontCam (<auto>) at resolution 1920x1080 in file mode
  ```
- Vérifier que l'exécution poursuit le chargement du modèle et le démarrage de la mesure sans lever d'exception.

## Régression
- Les autres modes (`device`, `webcam`) continuent d'envoyer les mêmes champs JSON.
- Les erreurs gRPC non liées à un objet manquant sont toujours remontées immédiatement.

## Actions complémentaires possibles
- Documenter dans la configuration d'équipe la liste des objets vidéo disponibles côté PROVEtech:TA.
- Automatiser un test de connexion qui liste les sources vidéo via l'API pour éviter la configuration manuelle.
