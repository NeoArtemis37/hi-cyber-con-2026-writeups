# The Miner That Mined The Victim

**HI Cyber Con 2026 · Forensics · Résolu**

## Énoncé et consignes

Résumé de l'énoncé conservé dans la transcription : une victime télécharge un prétendu optimiseur de minage, l'exécute, découvre des fichiers chiffrés et supprime le dossier du programme. Une collecte de triage du disque C est fournie pour reconstruire la chronologie et répondre à **14 questions**. L'énoncé avertit que la collecte peut contenir du logiciel malveillant actif.

## Artefacts

Le dépôt inclut les [faits extraits](../../artifacts/the-miner-that-mined-the-victim/input/facts.redacted.json) et la [transcription des 14 validations](../../artifacts/the-miner-that-mined-the-victim/input/transcript.redacted.txt). Les noms d'utilisateur, URL de diffusion du malware et identifiant du téléchargement ont été expurgés. Aucun échantillon exécutable n'est nécessaire à la lecture de ces résultats.

Les sources d'origine étaient l'historique du navigateur, Sysmon, le registre, le Prefetch, la MFT et la corbeille. Les [113 événements Sysmon du processus suspect](../../artifacts/the-miner-that-mined-the-victim/input/sysmon.miner.redacted.jsonl), les [enregistrements MFT sélectionnés](../../artifacts/the-miner-that-mined-the-victim/input/mft.selected.redacted.json) et le [Prefetch décompressé](../../artifacts/the-miner-that-mined-the-victim/input/miner-prefetch.raw) sont également fournis. Les deux exports JSON sont filtrés et expurgés ; le Prefetch conserve les chemins fictifs du scénario. Ce n'est pas une copie intégrale du triage.

## 1. Reconstituer la chronologie

Le registre donne `ActiveTimeBias = 420`, soit **UTC−7**. La date de téléchargement ne prouve pas l'exécution ; le Prefetch et les événements Sysmon complètent cette preuve.

| UTC, 13 mai 2026 | Constat |
| --- | --- |
| 14:25:36 | Téléchargement terminé |
| 14:26:55 | Première exécution documentée, une exécution recensée |
| 14:26:58 | Chargement de la bibliothèque de cryptographie .NET ; premières traces de chiffrement |
| 14:26:58 | Modification d'une valeur de stratégie Windows Defender |
| 14:27:01 | Fin du processus |
| 14:27:47 | Suppression du dossier retrouvée dans la corbeille |

L'analyse recense **34 fichiers** portant l'extension `.vibed`. Une autre tentative de modification de protection est refusée pour défaut d'accès ; elle ne doit pas être confondue avec la modification réussie.

## 2. Analyser les exports Sysmon, MFT et Prefetch

La commande suivante compte les créations `.vibed`, relève les événements de chargement de bibliothèque, de registre et de fin de processus, puis lit l'horodatage du Prefetch. Pour `bar.txt`, elle relie le SHA-256 de la suppression Sysmon au fichier archivé retrouvé dans les données résidentes MFT, puis vérifie l'empreinte du texte récupéré :

```bash
python3 artifacts/the-miner-that-mined-the-victim/scripts/analyze_exports.py
```

Sortie obtenue :

```text
Sysmon events: 113 IDs: {5: 1, 7: 41, 11: 36, 13: 1, 23: 34}
Distinct .vibed creations: 34
Registry value modified UTC: 2026-05-13 14:26:58.512 value: DWORD (0x00000001)
Crypto assembly loaded UTC: 2026-05-13 14:26:58.931
Process terminated UTC: 2026-05-13 14:27:01.944
Prefetch recorded execution timestamps: 1
Prefetch execution UTC: 2026-05-13 14:26:55.567595
Selected MFT records: 76 deleted: 0
Recovered deleted bar.txt (SHA-256 verified): I will always be there for you bro!
```

Le nombre de fichiers chiffrés est ainsi recalculé depuis les événements et la première exécution depuis le Prefetch ; ils ne sont pas simplement recopiés depuis `facts.redacted.json`. Le journal Sysmon ne contient pas ici d'événement de création du processus suspect : il faut donc croiser ces sources.

## 3. Contrôler les résultats du questionnaire

Prérequis : Python 3. Cette commande relit les extraits inclus et compte les confirmations de la transcription ; elle ne relance pas le questionnaire distant :

```bash
python3 artifacts/the-miner-that-mined-the-victim/scripts/inspect_evidence.py
```


Sortie obtenue lors de la reproduction locale :

```text
Timezone UTC offset (minutes): -420
Download completed UTC: 2026-05-13 14:25:36.833030
First execution UTC: 2026-05-13 14:26:55.567595
Encrypted files: 34
Correct answers: 14 / 14
FLAG hiCTF{c4r3ful_4b0ut_cr4ck3d_t001s_b7c76aa262}
```


## Résultat

```text
hiCTF{c4r3ful_4b0ut_cr4ck3d_t001s_b7c76aa262}
```

Un autre flag apparaît à la question 10 : c'est une réponse intermédiaire. Le résultat ci-dessus est annoncé après `All questions answered correctly!`.

Les commandes originales d'extraction du triage n'ont pas été conservées intégralement. Les commandes fournies réanalysent les exports inclus et vérifient la transcription ; elles ne reproduisent pas à elles seules toute l'enquête depuis le disque. La réponse `T1685` est celle acceptée dans la transcription historique, sans validation actuelle de la nomenclature MITRE.

[Retour à l’index](../../README.md)
