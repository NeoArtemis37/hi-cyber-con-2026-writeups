# Cairn

**HI Cyber Con 2026 · Cryptographie · Résolu**

## Énoncé et consignes

> One step at a time. Do not look back.

L'archive annoncée sur la plateforme est `cairn.zip`, SHA-256 `9f8f036fbb3a25341dc58602c9d8c340c786f1ba882095c45bac69b785796f21`. Le format attendu est `hiCTF{}`.

La spécification complète est fournie dans [RULES.md](../../artifacts/cairn/input/RULES.md). Il faut parcourir **1 048 576** états dans `GF(p²)`, dériver une clé de l'état final, puis déchiffrer et authentifier le flag avec AES-256-GCM.

## Artefacts

| Fichier fourni ou conservé | Taille (octets) | SHA-256 |
| --- | ---: | --- |
| [RULES.md](../../artifacts/cairn/input/RULES.md) | 3 742 | `b099195cc8bfc76c745a3191d26bf10d65734b45753c2217d6921a57929517b0` |
| [challenge.json](../../artifacts/cairn/input/challenge.json) | 7 715 | `a606acc0a44cd06687a82398634e21962af98391bc27ac1451e5ee4e714ad3f3` |
| [checkpoint_cpp.txt](../../artifacts/cairn/input/checkpoint_cpp.txt) | 475 | `249ea636c94ce80e3cbbd334cb7acdd54064c43bc2911a46a62598225b6705af` |

`checkpoint_cpp.txt` est un résultat de calcul conservé, distinct des fichiers distribués par l'organisateur. Les sources historiques [Python](../../artifacts/cairn/scripts/solve.py) et [C++](../../artifacts/cairn/scripts/solve.cpp) sont également fournies. Leur marche complète n'a pas été recalculée pour cette vérification.

## 1. Comprendre la marche

Chaque état est une paire `(a,b)`, sérialisée en deux entiers de 32 octets petit-boutistes. À l'étape `i`, le haché `SHA256(ser(j) || BE8(i) || salt)` choisit un degré parmi `2,3,5,7`, puis une racine du polynôme modulaire correspondant. Les racines doivent être triées lexicographiquement ; changer cet ordre change tout le parcours.

Le checkpoint final contient le nombre d'étapes et les deux composantes de `j_T`. On peut donc vérifier la dernière étape cryptographique sans refaire le parcours coûteux.

## Recalculer la marche complète

Pour repartir du début avec le [solveur Python fourni](../../artifacts/cairn/scripts/solve.py), installer ses dépendances puis lancer :

```bash
python3 -m pip install python-flint pycryptodome
python3 artifacts/cairn/scripts/solve.py 1048576
```

Cette commande est coûteuse. Le solveur écrit son checkpoint dans `artifacts/cairn/results/checkpoint.json` et reprend ce fichier s'il existe. La marche complète n'a pas été relancée pour cette édition. Le [dernier enregistrement du calcul natif historique](../../artifacts/cairn/results/historical-progress-final.txt) atteste l'arrivée à l'étape finale :

```text
step 1048576 elapsed 2407.47 rate 404.565 j 2951744835154356679408485058539998725114852725772335444978399055687248892073,76297261829986891261504719508868871098352200233656976244600190934732692176052
```

Le [source natif C++](../../artifacts/cairn/scripts/solve.cpp) est inclus pour cette version du calcul. La vérification GCM ci-dessous, elle, a été exécutée à nouveau avec le checkpoint final fourni.

## 2. Vérifier le checkpoint et déchiffrer

Prérequis : Python 3 et `cryptography`. Depuis la racine du dépôt :

```bash
python3 artifacts/cairn/scripts/decrypt_checkpoint.py
```

Le [script](../../artifacts/cairn/scripts/decrypt_checkpoint.py) impose `checkpoint_step == T`, calcule `SHA256(ser(j_T) || "IsogenyLabyrinth")`, puis vérifie l'étiquette GCM avant d'écrire le résultat.

Sortie obtenue lors de la reproduction locale :

```text
Checkpoint: 1048576 / 1048576
AES-GCM: authentication OK
FLAG hiCTF{w41k_th3_sup3rs1n9u14r_l46yr1ntH}
```


## Résultat

Le [flag extrait](../../artifacts/cairn/results/flag.txt) est authentifié par GCM. Le [journal historique](../../artifacts/cairn/results/historical-runner.txt) conserve aussi `VERIFIED FLAG`.

```text
hiCTF{w41k_th3_sup3rs1n9u14r_l46yr1ntH}
```

Le point critique est la sérialisation exacte : précision arbitraire des entiers, ordre des racines, 32 octets petit-boutistes par composante et indice grand-boutiste sur 8 octets.

[Retour à l’index](../../README.md)
