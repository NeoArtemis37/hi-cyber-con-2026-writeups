# No Bit Sings Alone

**HI Cyber Con 2026 · Stéganographie · Résolu sur la plateforme ; méthode finale non retrouvée**

## Énoncé et consignes

Le texte original de la page n'a pas été conservé. Le fichier fourni est `suspicious.wav` ; les analyses survivantes recherchent la clé d'une enveloppe AES-256-GCM dissimulée dans l'audio. Elles ne conservent pas le déchiffrement final.

## Artefacts

| Fichier fourni ou conservé | Taille (octets) | SHA-256 |
| --- | ---: | --- |
| [suspicious.wav](../../artifacts/no-bit-sings-alone/input/suspicious.wav) | 10 543 996 | `fc3d9d08017073b22d65fee816a62795bc760e1529fe914dd5e20c081186ed96` |

Les [glyphes transcrits](../../artifacts/no-bit-sings-alone/results/text-decoded.txt), le [rapport de reprise](../../artifacts/no-bit-sings-alone/results/resume-audio-report.txt) et deux journaux d'essais sont inclus.

## 1. Examiner le WAV

Prérequis : Python 3. Depuis la racine du dépôt :

```bash
python3 artifacts/no-bit-sings-alone/scripts/inspect_wav.py artifacts/no-bit-sings-alone/input/suspicious.wav
```


Sortie obtenue lors de la reproduction locale :

```text
channels: 2
sample_width_bytes: 2
sample_rate: 44100
frames: 2635988
duration_seconds: 59.772971
sha256: fc3d9d08017073b22d65fee816a62795bc760e1529fe914dd5e20c081186ed96
```


## 2. Transcrire et vérifier l'enveloppe

![Texte extrait du spectrogramme](../../artifacts/no-bit-sings-alone/results/text-clean.png)

La transcription indique l'algorithme, un nonce et six lignes `C0` à `C5`. La commande suivante vérifie leurs longueurs :

```bash
python3 artifacts/no-bit-sings-alone/scripts/inspect_envelope.py
```


Sortie obtenue lors de la reproduction locale :

```text
Algorithm: AES256GCM
Nonce bytes: 12
Ciphertext including tag bytes: 80
Authenticated key/flag: absent from retained results
```


Le texte chiffré complet fait **80 octets, étiquette comprise**. L'ancienne transcription à 66 octets était tronquée et ne doit pas être utilisée comme entrée AES-GCM.

## 3. Résultats des essais conservés

Le canal droit contient 58 tons dans les 58 derniers blocs complets de 4 096 trames. Plusieurs hypothèses combinent ces tons et des parités de blocs. Les [journaux inclus](../../artifacts/no-bit-sings-alone/results/subgroup-parity.txt) enregistrent un échec d'authentification dans les modèles testés ; le [contrôle de matrices FSK](../../artifacts/no-bit-sings-alone/results/fsk-bitmatrix.txt) est également négatif.

```bash
tail -n 1 artifacts/no-bit-sings-alone/results/subgroup-parity.txt
tail -n 1 artifacts/no-bit-sings-alone/results/fsk-bitmatrix.txt
```


Sorties conservées des deux commandes :

```text
tested 276480
tested 917504
```

## Résultat trouvé et limite

Le message spectral et les longueurs de l'enveloppe sont vérifiés. Aucune clé authentifiée ni flag final ne figure dans les résultats retrouvés. Les journaux négatifs bornent les modèles essayés ; ils ne démontrent pas qu'aucune autre extraction n'est possible.

[Retour à l’index](../../README.md)
