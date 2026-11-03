# ChronoGrind

**Cryptographie · résolu sur la plateforme · résolution finale absente des traces.**

## Énoncé et consignes

Le texte de présentation de la plateforme n'a pas été retrouvé. Le challenge fournit `state.dat` et `flag.enc` ; les consignes techniques sont embarquées dans `state.dat`. Elles décrivent un calcul séquentiel, une dérivation de clé et une vérification ChaCha20-Poly1305.

## Artefacts

- [Archive originale](../../artifacts/chronogrind/input/chronogrind.zip), 1 798 octets, SHA-256 `5a5316e688fdd9ee3ae30d85a5659a52d0a5c0adf74ac71ba95583467ac256b3`.
- [Paramètres récupérés](../../artifacts/chronogrind/input/params.json) et [paramètres pour le programme C](../../artifacts/chronogrind/input/params.txt).
- [Programme de calcul conservé](../../artifacts/chronogrind/scripts/solve.c), [checkpoint](../../artifacts/chronogrind/results/checkpoint.txt), [journal historique](../../artifacts/chronogrind/results/run.log).

Les commandes suivantes se lancent depuis la racine du dépôt. L'inspection utilise Python 3 et sa bibliothèque standard. Le programme C dépend des en-têtes et de la bibliothèque OpenSSL.

## 1. Retrouver les instructions dans `state.dat`

La couche d'obfuscation contient des chaînes XORées avec `0x4c`. Le script fourni lit l'archive, applique ce XOR et affiche les lignes de consigne :

```bash
python artifacts/chronogrind/scripts/extract_notes.py
```

Sortie reproduite lors de la préparation du dépôt :

```text
anchor = rec[11] (base241), seed = rec[22] (base241), cycles = rec[33] (decimal)
chk = rec[44] = sha256('anchor:seed:cycles' as decimal, colon-separated)[:8]
derivation: v = seed; repeat cycles times: v = v*v mod anchor
k = sha256(v as 256-byte big-endian)
msg container CGFX: magic 'CGFX'(4) ver(1) nonce(12) tag(16) ct(rest)
aead = chacha20-poly1305, key = k, nonce = nonce field
flag = aead_decrypt(k, nonce, ct); tag must verify
```

Ces lignes définissent le rôle des enregistrements et l'authentification attendue. Les fichiers de paramètres déjà décodés sont conservés dans `input/`.

## 2. Inspecter les paramètres et le point de reprise

```bash
python artifacts/chronogrind/scripts/inspect_state.py
```

```text
modulus_bits=2048
cycles=9000000000
checkpoint_iterations=6330000000
progress_percent=70.333333
container_magic=CGFX
container_version=1
container_bytes=68
ciphertext_bytes=35
saved_final_result_files=0
```

Le programme fait donc neuf milliards de carrés modulaires. Il emploie la représentation de Montgomery d'OpenSSL et sauvegarde un point de reprise tous les dix millions de tours.

## 3. Lire le résultat réellement conservé

```bash
tail -n 3 artifacts/chronogrind/results/run.log
```

```text
6310000000/9000000000 70.111111% 1109295 iterations/s ETA 2425.0s
6320000000/9000000000 70.222222% 1105919 iterations/s ETA 2423.3s
6330000000/9000000000 70.333333% 1105042 iterations/s ETA 2416.2s
```

Le dernier checkpoint couvre **70,333333 %** du calcul. Ce journal n'atteste pas l'achèvement et n'indique pas qu'un processus tourne encore.

## 4. Commande pour reprendre le calcul conservé

Le code attend un dossier contenant `params.txt`, `flag.enc` et éventuellement `checkpoint.txt`. Voici la commande de reproduction, reconstruite à partir de son interface ; le calcul complet n'a pas été relancé :

```bash
chrono_run_dir="$(mktemp -d)"
cp artifacts/chronogrind/input/params.txt artifacts/chronogrind/input/flag.enc "$chrono_run_dir/"
cp artifacts/chronogrind/results/checkpoint.txt "$chrono_run_dir/"
cc -O3 artifacts/chronogrind/scripts/solve.c -lcrypto -o "$chrono_run_dir/solve"
"$chrono_run_dir/solve" "$chrono_run_dir"
```

À l'arrivée, le programme sérialise la valeur sur 256 octets big-endian, calcule son SHA-256, puis vérifie le tag Poly1305. Il n'écrit `verified-flag.txt` et `result.json` qu'après cette vérification.

## Résultat

**Aucun flag final retrouvé dans ces artefacts.** Le statut final du compte est « résolu », mais la sortie authentifiée de la résolution n'a pas été conservée dans le corpus accessible. La dernière sortie disponible est le checkpoint à 6 330 000 000 tours.

[Retour à l'index](../../README.md)
