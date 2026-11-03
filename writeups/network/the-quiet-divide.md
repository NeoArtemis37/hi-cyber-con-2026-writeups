# The Quiet Divide

**HI Cyber Con 2026 · Network · Résolu**

## Énoncé et consignes

Le texte original de la page n'a pas été conservé. Le dossier demande de reconstruire un cas de production cohérent à partir de la capture réseau, d'une chaîne de conservation signée, d'un firmware et de coffres chiffrés, puis de récupérer le flag authentifié.

## Artefacts

| Fichier fourni ou conservé | Taille (octets) | SHA-256 |
| --- | ---: | --- |
| [the-quiet-divide.pcap](../../artifacts/the-quiet-divide/input/the-quiet-divide.pcap) | 152 240 093 | `20745719c71667df455e3bd68cd948d4dffbe3c68ac925dc991e2040411bdddc` |
| [deployed-codec.elf](../../artifacts/the-quiet-divide/input/deployed-codec.elf) | 14 528 | `0835dfce789d002d55f3d20fe7f953a30da0adbef336a861839ce8f579958836` |
| [quic-stream-0.json](../../artifacts/the-quiet-divide/input/quic-stream-0.json) | 403 | `dd2da0cceb4b8f337ea9b27c8df58848d9adde539a14ca4718970fe8bd802bd8` |

Le [sous-ensemble HTTP extrait](../../artifacts/the-quiet-divide/input/http_objects/) contient le comité, quinze événements, l'attestation, la trame, le checkpoint et les trois archives chiffrées. Il suffit pour reproduire la résolution ci-dessous. Les chemins `/api/...` présents dans ces objets sont des données de la capture ; aucune requête réseau n'est effectuée.

## Extraire les objets HTTP depuis la PCAP

Prérequis : Tshark. Le [script d'export](../../artifacts/the-quiet-divide/scripts/export_http.py) relit la capture, exporte les objets HTTP dans un répertoire temporaire et confronte leurs SHA-256 aux neuf entrées conservées dans le sous-ensemble :

```bash
python3 artifacts/the-quiet-divide/scripts/export_http.py
```

Il utilise cette commande Tshark, avec un dossier temporaire créé localement :

```bash
ctf_http_dir="$(mktemp -d)"
tshark -r artifacts/the-quiet-divide/input/the-quiet-divide.pcap --export-objects "http,$ctf_http_dir" -q
```

Sortie du contrôle réellement exécuté :

```text
HTTP objects exported: 215
HTTP bytes exported: 142291118
Retained inputs verified by SHA-256: 9/9
```

L'export complet contient aussi les objets de contexte et leurres. Les neuf fichiers utilisés par les étapes suivantes ont tous un correspondant identique dans la capture.

## 1. Vérifier les preuves avant de déchiffrer

Le [premier script](../../artifacts/the-quiet-divide/scripts/verify_signatures.py) vérifie les hachés, chaque lien parent, les signatures Ed25519, le quorum et la présence d'un président autorisé.

Le [second script](../../artifacts/the-quiet-divide/scripts/recover_archives.py) relie attestation, observation QUIC, firmware et lot d'archives au sceau. Il vérifie le CRC de la trame et restitue le compteur, la file, la charge et l'horodatage. Ces preuves alimentent HKDF-SHA256 ; les trois archives sont ouvertes uniquement si AES-GCM les authentifie.

## 2. Sélectionner la transaction et assembler les fragments

Le [troisième script](../../artifacts/the-quiet-divide/scripts/recover_flag.py) croise transferts et reçus dans les SQLite déchiffrées. Il impose une seule correspondance sur les engagements, le nonce, le compteur, l'origine, la version, le checkpoint et l'état observé. Quatre fragments ordonnés fournissent ensuite le matériau de la dérivation finale.

## 3. Reproduire la chaîne hors ligne

Prérequis : Python 3 et `cryptography`. Le [lanceur](../../artifacts/the-quiet-divide/scripts/reproduce.py) exécute les trois scripts dans un répertoire temporaire, puis conserve seulement le flag final :

```bash
python3 artifacts/the-quiet-divide/scripts/reproduce.py
```


Sortie obtenue lors de la reproduction locale :

```text
All 15 custody signatures valid; quorum, chair and parent chain valid through b34dc728c1fa1525020b1969a8af2698b2bcd91a95d58b3e3b940de35deda6e1
Decoded deployed state {'sequence': 10450910, 'scheduler_queue': 23, 'load': 71, 'epoch_ms': 1793517529318}
AUTHENTICATED vault-0.sqlite 4861952 b'SQLite format 3\x00\x10\x00\x01\x01'
AUTHENTICATED vault-1.sqlite 4861952 b'SQLite format 3\x00\x10\x00\x01\x01'
AUTHENTICATED vault-2.sqlite 4861952 b'SQLite format 3\x00\x10\x00\x01\x01'
UNIQUE EVIDENCE MATCH 2 6dd9ec588c9914ca95df44b2
AUTHENTICATED FLAG hiCTF{c8c46fdbd6e5e4eacabfba53a156ff9ab10567f2}
```


## Résultat

```text
hiCTF{c8c46fdbd6e5e4eacabfba53a156ff9ab10567f2}
```

Le [flag final](../../artifacts/the-quiet-divide/results/flag.txt) est conditionné à l'unicité de la transaction et à la réussite de GCM. La sérialisation JSON canonique fait partie du protocole : clés triées, séparateurs compacts, ASCII stable.

[Retour à l’index](../../README.md)
