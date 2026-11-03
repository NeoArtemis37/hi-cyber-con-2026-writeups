# The Reason for the Photograph

**OSINT · non résolu.**

## Énoncé et consignes

> Find where the observer stood. Look away from the clearing.

Le dialogue précise que le sujet important se trouve **derrière le photographe**. Un autre paragraphe décrit un sanctuaire nommé pour une religion qu'il n'a jamais servie, après confusion d'anciens mégalithes avec un lieu de prière.

La [consigne](../../artifacts/the-reason-for-the-photograph/statement.md) et une [capture complète du texte affiché](../../artifacts/the-reason-for-the-photograph/results/statement-and-rejection.png) sont incluses. Les notes indiquent une réponse composée du nom du lieu et d'une adresse what3words.

## Artefacts

- [Archive originale](../../artifacts/the-reason-for-the-photograph/input/challenge.zip), 2 020 906 octets, SHA-256 `186ac4022dd75e5538446758d0b8b2d26bac21362002a9b1b0c1aa2bce995d79`.
- [Image originale `place.jpg`](../../artifacts/the-reason-for-the-photograph/input/place.jpg), 2 034 606 octets.
- [Correspondance visuelle avec le panorama](../../artifacts/the-reason-for-the-photograph/results/panorama-match.png).
- [Mesures et points de contrôle](../../artifacts/the-reason-for-the-photograph/results/resection-observations.json), [rapport métrique complet](../../artifacts/the-reason-for-the-photograph/results/metric-report.txt) et vues de contrôle dans le même dossier.

![Image donnée dans le challenge](../../artifacts/the-reason-for-the-photograph/input/place.jpg)

## 1. Contrôler l'image fournie

Depuis la racine du dépôt :

```bash
sha256sum artifacts/the-reason-for-the-photograph/input/place.jpg
```

```text
5f52531caf55ec941ba924b026e0ea8b1c0909ced2bf7b7e3bcd9727ba3b6ef7  artifacts/the-reason-for-the-photograph/input/place.jpg
```

```bash
exiftool -s -ImageWidth -ImageHeight -GPSLatitude -GPSLongitude \
  -DateTimeOriginal artifacts/the-reason-for-the-photograph/input/place.jpg
```

Sortie reproduite :

```text
ImageWidth                      : 1456
ImageHeight                     : 720
```

Le fichier du challenge fait **1 456 × 720 pixels**. Il ne faut pas le confondre avec la sphère panoramique de référence de 8 704 × 4 352 pixels retrouvée ultérieurement. Les champs consultés n'exposent pas de GPS.

## 2. Identifier le site et la source visuelle

Les indices architecturaux et historiques pointent vers **Iglesia Vieja, Tonalá, Chiapas, Mexique**. La comparaison avec une sphère de mars 2023 attribuée à Víctor Nucamendi solorzano retrouve le même tronc incliné, les mêmes branches, la bordure circulaire et le bloc au sol :

![Panorama de référence retrouvé pendant l'enquête](../../artifacts/the-reason-for-the-photograph/results/panorama-match.png)

Identifiant de la sphère :

```text
CIHM0ogKEICAgICRyojqfg
```

La structure située derrière l'observateur a été associée au bâtiment B-3. La [fiche INAH du site](https://www.inah.gob.mx/zonas/zona-arqueologica-de-iglesia-vieja) et l'[étude archéologique d'Akira Kaneko](https://www.asociaciontikal.com/wp-content/uploads/2017/03/54.10-_Kaneko_rev.pdf) sont les références enregistrées dans les notes.

## 3. Écarter le simple point d'intérêt Maps

La position publiée pour la sphère coïncide avec un marqueur général du site. Elle ne démontre pas la position du photographe. La réponse construite avec l'adresse `amazes.communes.hairier` a été rejetée :

```text
The flag was incorrect.
```

La capture de l'énoncé conserve ce résultat. Il faut donc poursuivre la localisation au lieu d'adopter le marqueur du site.

## 4. Vérifier la calibration utilisée pour les mesures

Les notes ont d'abord corrigé une confusion : le paramètre de 75° correspond au champ **vertical**. Le rapport conserve une focale ajustée de 493,87 pixels, sur une vue de 1 048 × 758 pixels.

Le calcul suivant reproduit la conversion de cette focale en champs de vue, à partir de la mesure enregistrée :

```bash
python -c 'import math; f=493.87; print(f"vertical_fov={math.degrees(2*math.atan(758/(2*f))):.3f} deg"); print(f"horizontal_fov={math.degrees(2*math.atan(1048/(2*f))):.3f} deg")'
```

```text
vertical_fov=75.006 deg
horizontal_fov=93.391 deg
```

La résection utilise des directions vers des points homologues du panorama et du plan. Deux calages plausibles déplacent la caméra d'environ **4,6 mètres**. Le [rapport métrique](../../artifacts/the-reason-for-the-photograph/results/metric-report.txt) détaille ces mesures et l'incertitude sur les pieds de maçonnerie sous la végétation.

La première coordonnée provisoire, associée dans les notes à `redesigns.confronting.baskets`, est restée **non soumise** après ce contrôle. Elle n'est pas une réponse validée.

## Résultat

**Site et panorama identifiés ; point caméra et triplet what3words final non établis.** L'incertitude restante couvre plusieurs carrés what3words. Aucun flag n'est retenu et la plateforme affiche toujours le challenge comme non résolu.

Les captures et références conservent leurs crédits d'origine ; leur présence sert à documenter la comparaison, sans attribution d'une nouvelle licence.

[Retour à l'index](../../README.md)
