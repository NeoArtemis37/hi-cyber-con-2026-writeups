# Rocinate Revenge

**Cryptographie · non résolu.**

## Énoncé et consignes

Le texte de présentation de la plateforme n'a pas été retrouvé. Le [générateur fourni](../../artifacts/rocinate-revenge/input/chall.py) et son [jeu de données](../../artifacts/rocinate-revenge/input/chall.txt) sont conservés. Objectif reconstitué à partir du code : retrouver le secret `s`, qui est l'encodage entier du flag.

## Artefacts

- `chall.py` : générateur original, 715 octets.
- `chall.txt` : sortie originale, 248 810 octets, SHA-256 `30ea4c55181fdde73a05cdc8990f0c6e8663ab48c39b5c79a51edc111084db4e`.
- [Script d'inspection](../../artifacts/rocinate-revenge/scripts/inspect_challenge.py).
- [Contrôles historiques](../../artifacts/rocinate-revenge/results/review-checks.json), [recherche bornée de facteurs](../../artifacts/rocinate-revenge/results/bounded-factor-results.json) et [mesures LLL](../../artifacts/rocinate-revenge/results/measured-relations.json).

Toutes les commandes se lancent depuis la racine du dépôt. L'inspection fournie utilise uniquement la bibliothèque standard de Python 3 ; elle ne lance pas le générateur.

## 1. Lire la construction cryptographique

```bash
sed -n '1,80p' artifacts/rocinate-revenge/input/chall.py
```

Les lignes décisives du code sont :

```python
Cs = [secrets.randbelow(N) for _ in range(n)]
Zs = [ri*pow(s, ci, N) for ri, ci in zip(Rs, Cs)]
Ts = [pow(ri, e, N) for ri in Rs]
```

Les masques suivent une récurrence affine connue :

```text
R[i+1] = (a*R[i] + b) mod N
Z[i] = R[i] * (s^C[i] mod N)
T[i] = R[i]^e mod N
```

La multiplication qui produit `Z[i]` est entière : elle n'est pas réduite une seconde fois modulo `N`. L'exposant `e` n'est pas communiqué. Contrairement à Rocinate, les `C[i]` sont tirés par `secrets` ; la reconstruction de MT19937 n'est donc pas transposable.

## 2. Vérifier les dimensions et les raccourcis élémentaires

```bash
python artifacts/rocinate-revenge/scripts/inspect_challenge.py
```

Sortie reproduite à partir de `chall.txt` :

```json
{
  "N_bits": 2047,
  "n": 100,
  "smallest_C_bits": 2041,
  "smallest_nonzero_C_difference_bits": 2033,
  "gcd_a_N": 1,
  "gcd_b_N": 1,
  "gcd_a_minus_1_N": 1,
  "distinct_T": 100,
  "nontrivial_Z_N_gcds": []
}
```

Il y a cent échantillons, sans sortie `T` dupliquée. Les PGCD simples examinés ne donnent pas de facteur non trivial de `N`. Les exposants et leurs différences restent très grands.

## 3. Lire les résultats des recherches bornées

```bash
python -m json.tool artifacts/rocinate-revenge/results/bounded-factor-results.json
```

Extrait du résultat historique :

```json
{
  "fermat": {"iterations": 100000, "factors": null},
  "p_minus_1": {"bound": 100000, "factor": null, "gcd_equals_N": false}
}
```

Ces essais n'ont pas factorisé le module dans les bornes retenues. Ils ne prouvent pas qu'une factorisation soit impossible.

## 4. Mesurer la piste des relations entre exposants

Une piste examinée écrit `R[i] = A[i]*r0 + B[i] mod N`, puis cherche des relations entières entre les `C[i]`. Éliminer les puissances de `s` donnerait alors des contraintes polynomiales sur `r0`.

Les résultats d'une réduction LLL avaient été conservés. Pour en afficher les valeurs utiles, sans relancer ce calcul :

```bash
python -c 'import json; d=json.load(open("artifacts/rocinate-revenge/results/measured-relations.json")); print("exact_relations=",d["exact_relations"],sep=""); print("smallest_measured_degree=",min(x["degree"] for x in d["shortest"]),sep="")'
```

```text
exact_relations=99
smallest_measured_degree=38890977
```

Le degré minimal mesuré, **38 890 977**, rend la construction dense envisagée trop coûteuse pour constituer une résolution pratique. Ce constat ne ferme pas les autres pistes algébriques.

## Résultat

**Aucun flag récupéré.** Les vérifications et les résultats négatifs sont joints ; aucun solveur complet n'a été établi dans les traces retrouvées. Le challenge est également non résolu sur la plateforme au relevé final.

[Retour à l'index](../../README.md)
