# Operation Chimera

**Analyse réseau · résolu sur la plateforme · décodage final absent des traces.**

## Énoncé et consignes

Résumé du dossier de challenge, le texte exact de présentation n'ayant pas été retrouvé : analyser la capture fournie et remonter l'activité suspecte jusqu'au message caché. L'alerte SOC incluse signale un trafic DNS anormal après une connexion TLS. Le travail ci-dessous porte uniquement sur la PCAP fournie.

## Artefacts

- [Archive originale](../../artifacts/operation-chimera/input/operation_chimera.zip), 4 953 063 octets, SHA-256 `2f54e06473ae4ef3356a013209e402c26a88c000d630d73cece634865be453a0`.
- [Alerte SOC extraite](../../artifacts/operation-chimera/results/SEC-ALERT-49102.json).
- [Export EDNS historique](../../artifacts/operation-chimera/results/edns.tsv), [négociation TLS du flux 55](../../artifacts/operation-chimera/results/tls55.txt).
- [Script d'inspection PCAP](../../artifacts/operation-chimera/scripts/inspect_capture.py), [script de synthèse EDNS](../../artifacts/operation-chimera/scripts/summarize_edns.py).

Commandes depuis la racine du dépôt. Python 3 suffit aux scripts ; `unzip` et Tshark servent à refaire l'export réseau.

## 1. Contrôler le contenu de l'archive

```bash
python artifacts/operation-chimera/scripts/inspect_capture.py
```

Sortie reproduite depuis l'archive, sans extraire les 238 Mo sur disque :

```text
member=operation_chimera.pcap
pcap_bytes=238408692
frames=159069
pcap_sha256=9c8bbeb50d1348ae158f8a00632c95fe0867a9efbc521dfd7a2ef6698b12ebab
```

La capture comporte donc 159 069 trames. L'alerte décrit un poste `10.142.18.105` qui échange avec le DNS interne `10.142.18.1`, après une connexion à `delta.corp.internal`. Ces identifiants appartiennent au scénario fourni.

## 2. Exporter les options EDNS

La commande suivante lit la PCAP sur l'entrée standard et sélectionne l'option 65001 :

```bash
unzip -p artifacts/operation-chimera/input/operation_chimera.zip operation_chimera.pcap |
  tshark -r - -Y 'dns.opt.code == 65001' -T fields \
    -e frame.number -e dns.qry.name -e dns.opt.code -e dns.opt.data \
  > artifacts/operation-chimera/results/edns-reproduced.tsv
```

Puis synthétiser l'export conservé :

```bash
python artifacts/operation-chimera/scripts/summarize_edns.py
```

```text
edns_options=136
all_magic_CHIM=True
length_138_bytes=1
length_266_bytes=135
bytes_6_8_equal_41e8=31
option_codes=65001
```

Les options commencent toutes par `CHIM`. Les longueurs 266 et 138 octets, ainsi que les 31 occurrences de `41e8` aux offsets 6–7, sont des faits mesurés. Leur rôle dans l'en-tête n'a pas été démontré.

## 3. Examiner le flux TLS 55

Le [décodage TLS complet conservé](../../artifacts/operation-chimera/results/tls55.txt) permet de retrouver un client random composé de 32 octets `47`, une session de 32 octets `88` et ce server random :

```text
3c891e45aad02f81b7649e125088da7c913247f008c3296b8a714e5d2319bb04
```

Les reprises ont testé des combinaisons de ce random avec les fragments DNS et plusieurs modèles de LFSR, sans objet final authentifié. Le [résultat du contrôle linéaire GF(2)](../../artifacts/operation-chimera/results/header_gf2_results.json) et le [résultat d'une recherche de signature](../../artifacts/operation-chimera/results/known_file_bm_results.json) sont joints.

Un document HTTP contient un faux flag de QA explicitement signalé. Il ne constitue pas la réponse du challenge. Les signatures de compression apparues dans certains essais n'ont pas produit de flux complet validé.

## Résultat

**136 fragments `CHIM` localisés ; en-tête et transformation finale non décodés dans les notes conservées.** Aucun flag étayé ne peut être publié à partir de ces fichiers. Le statut final sur la plateforme est « résolu » ; l'étape ayant permis cette validation n'a pas été retrouvée.

[Retour à l'index](../../README.md)
