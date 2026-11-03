# HI Cyber Con 2026 — Writeups

**64/69 challenges · 4 019 points · 32e sur 1 119** — état final observé le 3 novembre 2026.

Writeups en français avec **consignes, fichiers du challenge, commandes, sorties et résultat obtenu**. Les 18 dossiers retrouvés comprennent 8 solutions et 10 analyses partielles. Les [69 challenges](docs/inventaire.md) sont inventoriés ; les méthodes des [51 autres](docs/lacunes.md) restent à retrouver.

## Reproduire une analyse

Les commandes des writeups se lancent depuis la racine du dépôt. Les fichiers nécessaires sont dans `artifacts/<challenge>/input/`, les scripts dans `scripts/` et leurs sorties dans `results/`. Chaque page précise ses dépendances.

Pour préparer un environnement Python commun aux scripts d'analyse :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Pour vérifier les fichiers inclus :

```bash
python3 scripts/verify_artifacts.py
```

Trois originaux volumineux sont fournis dans le paquet séparé `hi-cyber-con-2026-artifacts.tar`. Ils sont déjà présents dans le dossier de travail local. Après extraction du ZIP du dépôt ou clonage, on peut les restaurer et les vérifier :

```bash
python3 scripts/restore_artifacts.py ../hi-cyber-con-2026-artifacts.tar
python3 scripts/verify_artifacts.py --complete
```

Voir le [guide des artefacts](docs/artifacts.md) pour les fichiers inclus, les empreintes et le contenu du paquet.

## Solutions

| Challenge | Catégorie |
| --- | --- |
| [Cold Circuit](writeups/reverse/cold-circuit.md) | reverse |
| [Rocinate](writeups/crypto/rocinate.md) | crypto |
| [Cairn](writeups/crypto/cairn.md) | crypto |
| [Ghost in RAM](writeups/forensics/ghost-in-ram.md) | forensics |
| [The Miner That Mined The Victim](writeups/forensics/the-miner-that-mined-the-victim.md) | forensics |
| [Dead Air](writeups/misc/dead-air.md) | misc |
| [Low Tide Ledger](writeups/osint/low-tide-ledger.md) | osint |
| [The Quiet Divide](writeups/network/the-quiet-divide.md) | network |

## Analyses partielles

| Challenge | Catégorie | État final |
| --- | --- | --- |
| [Entitlement](writeups/reverse/entitlement.md) | reverse | Résolu ; méthode finale manquante |
| [ChronoGrind](writeups/crypto/chronogrind.md) | crypto | Résolu ; méthode finale manquante |
| [Rocinate Revenge](writeups/crypto/rocinate-revenge.md) | crypto | Non résolu |
| [chillin!!!](writeups/osint/chillin.md) | osint | Résolu ; méthode finale manquante |
| [The Reason for the Photograph](writeups/osint/the-reason-for-the-photograph.md) | osint | Non résolu |
| [Cipher](writeups/android/cipher.md) | android | Résolu ; méthode finale manquante |
| [Operation Chimera](writeups/network/operation-chimera.md) | network | Résolu ; méthode finale manquante |
| [Hall of Mirrors](writeups/steg/hall-of-mirrors.md) | steg | Résolu ; méthode finale manquante |
| [No Bit Sings Alone](writeups/steg/no-bit-sings-alone.md) | steg | Résolu ; méthode finale manquante |
| [Unremarable](writeups/steg/unremarable.md) | steg | Non résolu |

## Repères

- [Inventaire et auteurs des 69 challenges](data/challenges.json).
- [Consignes de rédaction et lecture des sorties](docs/format-writeup.md).
- [Sources et vérifications](docs/provenance.md).
- [Empreintes des sources historiques](data/sources.json).

Les énoncés originaux sont reproduits lorsqu’ils ont été retrouvés. Les énoncés incomplets et les résumés sont identifiés dans les pages concernées. Les résultats relancés localement sont distingués des journaux historiques.

Le dépôt Git local utilise la branche `main`. Aucun dépôt distant n’est configuré et rien n’a été publié sur GitHub.
