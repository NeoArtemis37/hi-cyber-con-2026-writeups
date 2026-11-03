# Cipher

**HI Cyber Con 2026 · Android · Résolu sur la plateforme ; méthode finale non retrouvée**

## Énoncé et consignes

Le texte original de la page n'a pas été conservé. Le fichier fourni est `cipher.apk`, paquet `com.hictf26.cipher`, version 1.0. L'analyse conservée inspecte un coffre chiffré embarqué et les ressources qui le décrivent. Elle ne conserve pas la phrase ni le déchiffrement final.

## Artefacts

| Fichier fourni ou conservé | Taille (octets) | SHA-256 |
| --- | ---: | --- |
| [cipher.apk](../../artifacts/cipher/input/cipher.apk) | 38 969 | `ae3e73403013f301378e82535ead07679bc1195f87ae3b14778e3cd0c19a9a84` |

Le [script d'inventaire](../../artifacts/cipher/scripts/static_inventory.py) lit l'APK comme une archive ZIP. Il n'installe et ne lance pas l'application. Le [résultat JSON complet](../../artifacts/cipher/results/inventory.json) est inclus.

## 1. Parser les ressources et les libellés d'algorithmes

Prérequis : Python 3, bibliothèque standard uniquement. Depuis la racine du dépôt :

```bash
python3 artifacts/cipher/scripts/static_inventory.py
```


Sortie obtenue lors de la reproduction locale :

```text
{
  "apk_sha256": "ae3e73403013f301378e82535ead07679bc1195f87ae3b14778e3cd0c19a9a84",
  "vault": {
    "magic": "V1LT",
    "version": 3,
    "salt_bytes": 16,
    "record_count": 64,
    "parsed_bytes": 6101,
    "unique_indices": 64,
    "ciphertext_length_range": [
      67,
      102
    ]
  },
  "dictionary": {
    "entries": 256,
    "entry_bytes": 8,
    "first_four": [
      "jkmqbtci",
      "rcnlrukw",
      "xeoctydy",
      "oziszvhi"
    ],
    "last_four": [
      "heselgqz",
      "wfmqvdvu",
      "elgzhjze",
      "gsozhaea"
    ]
  },
  "algorithm_labels": {
    "cipher": "AES/GCM/NoPadding",
    "mac": "HmacSHA256",
    "key_derivation": "PBKDF2WithHmacSHA256"
  },
  "plaintext_flag_pattern_matches": {},
  "activity": "Static resource parsing only; no candidate passwords or keys generated or tested."
}
```


Les fichiers `res/raw/p7.bin`, `m4.bin` et `n3.bin` correspondent respectivement au coffre, au dictionnaire masqué et à une référence de contrôle. Le script consomme exactement les **6 101 octets** du coffre : 64 enregistrements, 64 identifiants et des chiffrés de 67 à 102 octets.

## 2. Interpréter le résultat

La chaîne statique constatée utilise PBKDF2-HMAC-SHA256, 32 768 itérations et 256 bits, une vérification HMAC, puis une dérivation par enregistrement et AES-GCM. Le dictionnaire de 256 mots publics est décodé, mais ne livre aucun flag en clair.

La classe de compatibilité et la constante `cipher-verifier-v3` ne constituent pas une phrase secrète. Les différences de longueur de certains enregistrements ne permettent pas de déduire leur contenu.

## Résultat trouvé et limite

L'inventaire et les algorithmes sont vérifiés ; `plaintext_flag_pattern_matches` est vide. Aucun flag ni déchiffrement authentifié n'est établi par cette analyse statique. La méthode finale employée pour la validation du compte n'a pas été retrouvée.

[Retour à l’index](../../README.md)
