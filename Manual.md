# Guide de test automatisé

Ce projet contient un script `automate_test.py` qui s'appuie sur les
définitions Protobuf fournies dans `AutomatedAITest/testautomation_pb2.py`.

## Prérequis

* Python 3.9 ou supérieur.
* Le paquet `protobuf` (version 4 ou ultérieure est prise en charge par les
  correctifs récents).

Installez la dépendance principale avec :

```bash
pip install protobuf
```

## Notes de compatibilité

* Les versions récentes de `protobuf` (> 5) ont supprimé la méthode
  `GetPrototype`. Le module `testautomation_pb2.py` a été mis à jour pour
  utiliser automatiquement l'API `GetMessageClass`, assurant ainsi la
  compatibilité avec Python 3.9.5 et les bibliothèques actuelles.
* Si vous rencontrez des erreurs liées à des versions plus anciennes de
  `protobuf`, assurez-vous de réinstaller le paquet ou de nettoyer votre
  environnement virtuel.

## Exécution

```bash
python AutomatedAITest/automate_test.py
```

Le script devrait maintenant s'exécuter sans lever d'exception liée aux
imports Protobuf.
