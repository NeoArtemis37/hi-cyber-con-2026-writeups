# Unremarable

**Stéganographie · non résolu.** Le titre reprend l'orthographe publiée par la plateforme.

## Énoncé et consignes

> The file was recovered without any accompanying notes. Nothing about it was considered significant at the time.

Format demandé : `hiCTF{}`. La [transcription de la consigne](../../artifacts/unremarable/statement.md) est incluse.

## Artefacts

- [Archive originale `unremarkable.zip`](../../artifacts/unremarable/input/unremarkable.zip), SHA-256 `99f938ce777e48397f9b1ca5fbf422a8c90554086487e9169250a6996c30116e`.
- `chall.png` dans cette archive : PNG RGB de **4 725 × 3 150 pixels**.
- [Filtres extraits](../../artifacts/unremarable/results/filters.bin), [flux zlib de première couche](../../artifacts/unremarable/results/decoded.bin), [descripteur AFT2](../../artifacts/unremarable/results/payload.bin).
- [Extracteur AFT2](../../artifacts/unremarable/scripts/extract_aft2.py) et [contrôle du masque Sobel](../../artifacts/unremarable/scripts/inspect_component.py).

Commandes depuis la racine du dépôt. L'extracteur AFT2 utilise seulement Python 3 ; le contrôle des pixels demande Pillow, NumPy et SciPy.

## 1. Chercher une structure dans les filtres PNG

Les conteneurs ZIP et PNG ne contiennent pas de fichier ajouté après leur fin. La première piste utile est la succession des filtres de lignes : les **345 premiers filtres** diffèrent de la suite canonique observée ensuite.

Pour décoder cette couche directement depuis l'archive :

```bash
python artifacts/unremarable/scripts/extract_aft2.py \
  --archive artifacts/unremarable/input/unremarkable.zip \
  --output artifacts/unremarable/results/payload-reproduced.bin
```

Sortie reproduite :

```text
filter_bytes=3150
base5_digits=344
zlib_bytes=86
payload_bytes=85
magic=AFT2
crc32_stored=0x3e7d9217
crc32_calculated=0x3e7d9217
crc_valid=true
component_size_field=629487
```

L'extraction calcule les différences successives modulo 5 : 345 filtres donnent 344 chiffres. Quatre chiffres en base 5 forment un octet, soit 86 octets. La décompression zlib restitue les 85 octets du descripteur `AFT2`.

Le CRC32 de ce descripteur vaut `0x3e7d9217` et est valide. Pour comparer le résultat recalculé à l'artefact historique :

```bash
cmp artifacts/unremarable/results/payload.bin \
    artifacts/unremarable/results/payload-reproduced.bin
```

**Résultat :** code de retour 0, sans différence.

Pour rejouer seulement le décodage des filtres déjà extraits :

```bash
python artifacts/unremarable/scripts/extract_aft2.py \
  --filters artifacts/unremarable/results/filters.bin
```

## 2. Utiliser le descripteur pour sélectionner les pixels

Les premiers champs interprétés définissent le masque des deux bits faibles, les poids de luminance, les noyaux Sobel, un seuil et un point de départ. La luminance est :

```text
gray = ((R & 252)*77 + (G & 252)*150 + (B & 252)*29) >> 8
```

Le masque retient une magnitude Sobel L1 au moins égale à 114, exclut le bord et sélectionne la composante à huit voisins contenant `(x=3319, y=2198)`.

```bash
python artifacts/unremarable/scripts/inspect_component.py \
  artifacts/unremarable/input/unremarkable.zip
```

Sortie reproduite :

```text
red_lsb_decoy=hiCTF{fake flag-> nahh_m4n_this_n0t_that_easy}
seed_x=3319
seed_y=2198
connectivity=8
sobel_threshold=114
component_pixels=629487
rowmajor_index_crc32=0x6b4fb872
```

Les **629 487 pixels** correspondent exactement au champ de taille du descripteur. Cette correspondance confirme le masque et la composante.

La première ligne montre également le message trouvé dans le LSB rouge. Il se déclare lui-même faux : il s'agit d'un leurre, pas du flag du challenge.

## 3. Délimiter ce qui reste à comprendre

Les reprises historiques ont exploré les parcours BFS/DFS, les ordres de voisinage, les canaux R1/G0, les ordres de bits et plusieurs interprétations des groupes de sept. Elles n'ont pas obtenu de flag vérifié.

Le CRC des indices en ordre ligne, `0x6b4fb872`, ne correspond pas au champ `0xef36caaa` dont le rôle était supposé dans les notes. Le fait de pouvoir construire un candidat respectant un CRC ne suffirait pas à authentifier les hypothèses de transport.

La géométrie des modifications G0 est compatible avec au plus un changement par groupe de sept. Le sens du flux produit et son lien avec R1 restent inconnus.

## Résultat

**Première couche AFT2 décodée et vérifiée ; composante de 629 487 pixels reproduite ; vrai flag non retrouvé.** Le challenge demeure non résolu sur la plateforme. Le seul `hiCTF{...}` lisible directement est le leurre explicite montré ci-dessus.

[Retour à l'index](../../README.md)
