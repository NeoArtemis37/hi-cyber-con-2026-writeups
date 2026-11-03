# Entitlement

**HI Cyber Con 2026 · Reverse Engineering · Résolu sur la plateforme ; méthode finale non retrouvée**

## Énoncé et consignes

Le texte original de la page n'a pas été conservé. L'archive fournit un exécutable ELF x86-64 nommé `Entitlement`. Les traces retrouvées couvrent la préparation de son analyse et un fichier décompressé, sans entrée acceptée ni flag final.

## Artefacts

| Fichier fourni ou conservé | Taille (octets) | SHA-256 |
| --- | ---: | --- |
| [Entitlement.packed](../../artifacts/entitlement/input/Entitlement.packed) | 15 048 | `364e0b0cb9563702f5a30df2447dcc39c5550450a52a18085526bf2aced6cd14` |
| [Entitlement.unpacked](../../artifacts/entitlement/input/Entitlement.unpacked) | 27 224 | `7de224a007c5eac93b5331407b0bbd3c22d75d644e8f3b167dc87ab5aac86631` |

`Entitlement.packed` est l'original renommé pour le distinguer du résultat intermédiaire `Entitlement.unpacked`. Le nom de ce dernier décrit son origine historique ; la compilation ne refait pas la décompression.

## 1. Contrôler les fichiers sans les exécuter

Prérequis : Python 3. La commande lit les en-têtes ELF et calcule les empreintes :

```bash
python3 artifacts/entitlement/scripts/inspect_elf.py
```


Sortie obtenue lors de la reproduction locale :

```text
Entitlement.packed
  bytes: 15048
  sha256: 364e0b0cb9563702f5a30df2447dcc39c5550450a52a18085526bf2aced6cd14
  ELF class: 64
  entry: 0x40abd8
  UPX marker present: False
Entitlement.unpacked
  bytes: 27224
  sha256: 7de224a007c5eac93b5331407b0bbd3c22d75d644e8f3b167dc87ab5aac86631
  ELF class: 64
  entry: 0x4016d0
  UPX marker present: False
```


Le changement de taille et du point d'entrée montre que les deux fichiers sont différents. L'absence de chaîne `UPX` dans les octets ne suffit pas à déduire l'absence d'un empaquetage modifié.

## 2. Poursuivre l'inspection statique

Avec GNU binutils, le désassemblage peut être obtenu sans lancer le programme :

```bash
objdump -d artifacts/entitlement/input/Entitlement.unpacked > artifacts/entitlement/results/unpacked.asm
```


Cette commande produit du désassemblage, pas un flag. La logique complète de validation et l'entrée qui l'aurait satisfaite ne sont pas établies dans les sources retrouvées.

## Résultat trouvé et limite

Les deux ELF sont fournis avec leurs empreintes et leur point d'entrée. Le résultat final de résolution est absent ; cette page reste une analyse partielle malgré le statut résolu du compte.

[Retour à l’index](../../README.md)
