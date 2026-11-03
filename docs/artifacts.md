# Artefacts et reproduction

Les writeups se lisent avec leurs fichiers dans `artifacts/<challenge>/`. Les chemins des commandes partent de la racine du dépôt.

| Dossier | Contenu |
| --- | --- |
| `input/` | Archives et fichiers d'entrée, ou extraits/checkpoints explicitement décrits dans la page |
| `scripts/` | Scripts d'analyse, d'extraction, de décodage et de vérification |
| `results/` | Sorties enregistrées, flags, images produites et résultats intermédiaires |
| autres images | Captures d'énoncé, comparaisons et preuves visuelles |

L'[inventaire JSON](../artifacts/index.json) contient le chemin, le rôle, la taille et le SHA-256 de chaque fichier. [SHA256SUMS](../artifacts/SHA256SUMS) permet également un contrôle avec les outils usuels.

## Fichiers inclus dans le ZIP du dépôt

Les petites archives originales, images, données de challenge, binaires de reverse et extraits utiles accompagnent les scripts. Le WAV de No Bit Sings Alone, l'archive d'Unremarable, les captures d'énoncé disponibles et les images du journal Dead Air sont inclus.

Les dépendances et outils nécessaires sont indiqués dans chaque writeup. Certaines analyses se reproduisent avec la bibliothèque standard Python ; d'autres utilisent notamment `cryptography`, Pillow, NumPy, SciPy, Tshark, 7-Zip ou les outils ELF. Les fichiers `requirements.txt` présents sont propres aux scripts du challenge concerné.

## Paquet d'artefacts volumineux

Le paquet `hi-cyber-con-2026-artifacts.tar`, à côté du ZIP du dépôt, contient :

| Chemin restauré | Taille |
| --- | ---: |
| `artifacts/ghost-in-ram/input/ghost-in-ram.zip` | 1 693 016 017 octets |
| `artifacts/hall-of-mirrors/input/hall-of-mirrors.wav` | 299 520 216 octets |
| `artifacts/the-quiet-divide/input/the-quiet-divide.pcap` | 152 240 093 octets |

Ces fichiers sont présents dans le dossier local de travail. Ils sont ignorés par Git et séparés du ZIP léger. Pour une publication, le paquet peut accompagner le dépôt comme fichier à télécharger.

Après récupération des deux paquets, depuis la racine du dépôt :

```bash
python3 scripts/restore_artifacts.py ../hi-cyber-con-2026-artifacts.tar
python3 scripts/verify_artifacts.py --complete
```

Le script de restauration refuse les membres inattendus et vérifie chaque empreinte avant de remplacer le fichier local. Pour contrôler uniquement la distribution légère, en autorisant l'absence du paquet :

```bash
python3 scripts/verify_artifacts.py
```

## Résultats et limites

Les résultats complets sont accompagnés de leurs flags. Les enquêtes non abouties fournissent leurs sorties intermédiaires. Un extrait mémoire, un checkpoint ou un export de journaux ne remplace pas l'ensemble du fichier source ; la page le précise quand c'est le cas.
