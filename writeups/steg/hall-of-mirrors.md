# Hall of Mirrors

**HI Cyber Con 2026 · Stéganographie · Résolu sur la plateforme ; méthode finale non retrouvée**

## Énoncé et consignes

Le texte original de la page n'a pas été conservé. Le support est un enregistrement stéréo intitulé *Hall of Mirrors*. Le travail conservé consiste à rechercher les données cachées dans le spectre puis dans les échantillons audio. Cette page présente les étapes effectivement retrouvées, sans attribuer un flag final aux essais négatifs.

## Artefacts

| Fichier fourni ou conservé | Taille (octets) | SHA-256 |
| --- | ---: | --- |
| [hall-of-mirrors.wav](../../artifacts/hall-of-mirrors/input/hall-of-mirrors.wav) | 299 520 216 | `6468cb14b4eb578fe913a9c5d7af9d92deb83acb5265ac5c8817ed8e85e22a1c` |

La [note de travail complète](../../artifacts/hall-of-mirrors/results/STATUS.txt), les [fréquences détectées](../../artifacts/hall-of-mirrors/results/decode.txt) et les deux images spectrales ci-dessous sont incluses.

## 1. Vérifier le format audio

Prérequis : Python 3. Depuis la racine du dépôt :

```bash
python3 artifacts/hall-of-mirrors/scripts/inspect_wav.py artifacts/hall-of-mirrors/input/hall-of-mirrors.wav
```


Sortie obtenue lors de la reproduction locale :

```text
channels: 2
sample_width_bytes: 2
sample_rate: 48000
frames: 74880000
duration_seconds: 1560.000000
sha256: 6468cb14b4eb578fe913a9c5d7af9d92deb83acb5265ac5c8817ed8e85e22a1c
```


## 2. Lire le message spectral

Les notes situent le signal vers **1 180–1 246 secondes**. Le calcul historique emploie une STFT de 8 192 points, un pas de 4 096 et un contraste obtenu en retranchant la médiane locale sur 21 bins. Deux bandes portent chacune quatorze tons, soit sept lignes doublées d'une police 5×7.

Prérequis supplémentaires pour cette étape : NumPy, SciPy et Pillow. Le [script fourni](../../artifacts/hall-of-mirrors/scripts/extract_spectral.py) recalcule les deux grilles depuis le WAV :

```bash
python3 artifacts/hall-of-mirrors/scripts/extract_spectral.py
```

Sortie obtenue :

```text
Band 0: 14 carrier rows -> results/regenerated-band-0.png
Band 1: 14 carrier rows -> results/regenerated-band-1.png
```

![Clé lue dans le spectre](../../artifacts/hall-of-mirrors/results/regenerated-band-0.png)

![Protocole lu dans le spectre](../../artifacts/hall-of-mirrors/results/regenerated-band-1.png)

Transcription visible sur ces images :

```text
K=9C4F1E7A3B50D682
MIRRORS1  SM64/GAP/PAR
```

## 3. Distinguer le leurre du résultat

La note conservée décrit un flag apparent dans les LSB des mots 16 bits entrelacés. Le bilan de soumission l'identifie comme rejeté :

```text
hiCTF{just_lsb_n0ise}
```

Les variantes testées de SplitMix64, gaps et parités ne donnent pas de structure finale vérifiée. Pour lire le domaine exact des essais et leurs limites :

```bash
head -n 1 artifacts/hall-of-mirrors/results/STATUS.txt
```

```text
Hall of Mirrors — reprise documentée, aucun flag vérifié.
```


## Résultat trouvé et limite

Le résultat établi est le message spectral et sa clé. La méthode permettant d'obtenir le flag accepté ensuite sur la plateforme n'est pas présente dans les traces. Aucun vrai flag final n'est publié pour ce dossier.

[Retour à l’index](../../README.md)
