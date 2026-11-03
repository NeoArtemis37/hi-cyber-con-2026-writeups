# Cold Circuit

**HI Cyber Con 2026 · Reverse Engineering · Résolu**

## Énoncé et consignes

Le texte original de la page n'a pas été conservé. La tâche reconstituée à partir du binaire est de retrouver les **16 octets d'entrée** acceptés, puis de les encoder en hexadécimal dans `hiCTF{...}`.

## Artefacts

| Fichier fourni ou conservé | Taille (octets) | SHA-256 |
| --- | ---: | --- |
| [check](../../artifacts/cold-circuit/input/check) | 14 472 | `d99879bcf25e081c8383578718b227a705c81855688874b286c97e7fcca19610` |

Le binaire est fourni pour lecture statique. La méthode ci-dessous lit ses tables et n'exécute pas `check`.

## 1. Extraire la transformation

Le [solveur](../../artifacts/cold-circuit/scripts/solve.py) lit quatre zones : S-box de 256 octets à `0x2020`, permutation à `0x2120`, vingt clés de tour à `0x2140` et cible à `0x2280`.

Un tour effectue :

```text
y[perm[i]] = sbox[(x[i] + key[round,i]) mod 256]
```

La S-box et la permutation étant bijectives, le tour inverse est :

```text
x[i] = (inverse_sbox[y[perm[i]]] - key[round,i]) mod 256
```

## 2. Inverser les vingt tours et vérifier

Prérequis : Python 3, bibliothèque standard uniquement. Depuis la racine du dépôt :

```bash
python3 artifacts/cold-circuit/scripts/solve.py
```

Le script part de la cible, remonte les tours 19 à 0, puis rejoue les vingt tours dans le sens normal. Il exige une égalité exacte avec la cible.

Sortie obtenue lors de la reproduction locale :

```text
FLAG hiCTF{6e305f6a7461675f6e65656465642121}
VERIFIED all 20 forward rounds, target 976714880a500d160a21f6950eef3481
```


## Résultat

```text
hiCTF{6e305f6a7461675f6e65656465642121}
```

Le [fichier résultat](../../artifacts/cold-circuit/results/flag.txt) est généré par la commande. Les prédicats fondés sur `n² mod 4` sont opaques : ils ne créent pas de chemin supplémentaire dans les tables inversées.

[Retour à l’index](../../README.md)
