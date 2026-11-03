# chillin!!!

**OSINT · résolu sur la plateforme · réponse finale absente des traces.**

## Énoncé et consignes

> This looks scary!! Am I tripping?? Where is this actually? yo!, get me the name and exact three words for this location.

Format : `hiCTF{city_country_word1.word2.word3}`. La demande porte sur le lieu et ses trois mots exacts ; elle n'impose pas expressément de retrouver la caméra.

La [consigne transcrite](../../artifacts/chillin/statement.md) et la [capture historique de la plateforme](../../artifacts/chillin/results/w3w-landmark-rejected.png) sont fournies.

## Artefacts

- [Archive originale `chillin.zip`](../../artifacts/chillin/input/chillin.zip), 140 053 octets, SHA-256 `739b2ecb2dfc823b786301de1022f0ea890f12af80ea1e38319206286c0157ec`.
- [Photographie extraite `file.jpg`](../../artifacts/chillin/input/file.jpg), 140 054 octets.
- [Contrôle historique de l'image](../../artifacts/chillin/results/artifact-verification.json), [sortie EXIF reproduite](../../artifacts/chillin/results/exif.txt) et preuve du candidat rejeté.

![Photographie donnée dans le challenge](../../artifacts/chillin/input/file.jpg)

## 1. Vérifier le fichier

Commandes depuis la racine du dépôt, avec `sha256sum` et ExifTool :

```bash
sha256sum artifacts/chillin/input/file.jpg
```

```text
98a6d17ca2c5628e7657aa1a77247920fd2f7f70f8f28d40a2c93d405cfb71f1  artifacts/chillin/input/file.jpg
```

```bash
exiftool -s -ImageWidth -ImageHeight -GPSLatitude -GPSLongitude \
  -DateTimeOriginal artifacts/chillin/input/file.jpg
```

Sortie reproduite :

```text
ImageWidth                      : 907
ImageHeight                     : 590
```

L'image fait **907 × 590 pixels**. Ces champs ne donnent ni coordonnées GPS ni date d'origine ; il faut donc chercher à partir de la scène.

## 2. Comparer les indices visuels

La photographie montre un parvis très fréquenté à la nuit tombante, des lumières au sol, de hautes parois de grès et un aménagement de café. Ces éléments ont conduit à l'hypothèse du **Trésor, Al-Khazneh, à Pétra en Jordanie**.

Les notes ont comparé les falaises, les talus et les toitures. Elles ont écarté une photosphère diurne d'Ancient Jordan comme original exact. Une photosphère de Christian Paulsson, datée de mars 2018, servait de comparaison de relief ; son emplacement ne démontrait pas celui attendu par le challenge.

Les références historiques sont la [vue Ancient Jordan](https://ancientjordan.com/360-photo/petra-al-khazneh-the-treasury-360-photo/) et la [photographie du café par Gerd Eichmann](https://commons.wikimedia.org/wiki/File:Petra-Khazne_al-Firaun-18-Cafe-2010-gje.jpg). Elles sont citées comme pistes utilisées pendant l'enquête, sans nouvelle recherche effectuée pour ce dépôt.

## 3. Conserver le résultat de la tentative

Un candidat fondé sur un point public de Pétra a été rejeté. La capture conserve à la fois l'énoncé et le message de la plateforme :

![Énoncé et candidat rejeté pendant le CTF](../../artifacts/chillin/results/w3w-landmark-rejected.png)

```text
The flag was incorrect.
```

Le rejet porte sur la réponse complète. Il ne permet pas d'isoler une erreur sur le nom, le pays ou le triplet what3words, et ne suffit pas à exclure Pétra.

## Résultat

**Lieu proposé dans les notes : le secteur du Trésor à Pétra ; aucun triplet final vérifié dans les traces.** Le compte affiche ensuite le challenge comme résolu, mais la réponse acceptée n'a pas été retrouvée. Aucun flag précis ne peut être reconstitué à partir du seul candidat rejeté.

[Retour à l'index](../../README.md)
