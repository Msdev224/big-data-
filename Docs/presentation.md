# Présentation soutenance — Bookshop Big Data

**Durée cible : 15-20 min (10 min présentation + 5-10 min démo + Q/R)**
**Auteur : Mamadou Saidou Bah — Master 2 Big Data — Avril 2026**

Ce document déroule la soutenance étape par étape. Pour chaque moment : **quoi montrer**, **où c'est**, **ce que tu dis**, **ce que tu fais**.

---

## ⚙️ Préparation avant d'entrer en salle (T-15 min)

À faire une fois pour toutes avant d'ouvrir la porte :

```bash
cd /Users/msdev224/Desktop/big_data

# 1. Démarrer toute la stack
make up            # ou : docker compose up -d

# 2. Vérifier que les 4 conteneurs sont up
docker compose ps
# → postgres, airflow-webserver, airflow-scheduler, streamlit doivent être "running"

# 3. Faire un run "à blanc" du DAG pour que tout soit déjà vert
docker compose exec -T airflow-webserver airflow dags trigger bookshop_pipeline
sleep 45

# 4. Ouvrir les 4 onglets navigateur dans CET ordre
open http://localhost:8080          # Airflow (admin / cf. .env)
open http://localhost:8501          # Streamlit
open https://app.snowflake.com/NCNXBCK/DG28934   # Snowsight (MSDEV / mot de passe .env)
open https://github.com/<ton-user>/bookshop-bigdata   # Repo GitHub
```

Ouvrir aussi dans ton IDE le dossier `/Users/msdev224/Desktop/big_data` et un terminal **dans ce dossier**.

Raccourcis navigateur : `⌘+1` Airflow · `⌘+2` Streamlit · `⌘+3` Snowsight · `⌘+4` GitHub.

---

## 🎤 0. Ouverture (30 s)

**Affiche à l'écran :** slide 1 du PowerPoint ([docs/presentation.pdf](presentation.pdf)).

**Tu dis :**
> « Bonjour, je présente **Bookshop Analytics**, un pipeline Big Data de bout en bout qui ingère des données transactionnelles d'une librairie depuis PostgreSQL, les transforme dans Snowflake via dbt, et les expose dans un dashboard Streamlit. L'ensemble est orchestré par Airflow et reproductible avec Docker Compose. »

---

## 🔸 1. Contexte & problématique (1 min)

**Affiche :** slide 2 du PDF.

**Tu dis :**
- Source : base OLTP PostgreSQL, optimisée métier, pas pour l'analyse.
- Besoin : agrégats temporels, historisation, croisements → impossible en prod.
- Cible : KPI accessibles sans SQL, rafraîchis automatiquement.

---

## 🔸 2. Objectifs (1 min)

**Affiche :** slide 3.

**Tu dis :**
- Pipeline automatisé (1 clic / programmable).
- Stack cloud moderne (Snowflake + dbt).
- Reproductibilité totale (`make up`).
- Observabilité (logs structurés, tests, CI).

---

## 🔸 3. Architecture (1,5 min)

**Affiche :** slide 4.

**Tu expliques en pointant le flux :**
```
PostgreSQL  →  Airflow  →  Snowflake  →  dbt  →  Streamlit
(source)    (orchestr.) (RAW → STG →  WH →  MARTS)  (dashboard)
```

**Tu insistes sur :** les 4 couches Snowflake (RAW, STAGGING, WAREHOUSE, MARTS) qui matérialisent le pattern **Medallion** (bronze / silver / gold).

---

## 🔸 4. Stack technique (1 min)

**Affiche :** slide 5 (tableau techno).

**Tu dis en survol :** PostgreSQL 15 · Airflow 2.10 · Snowflake · dbt 1.9 · Streamlit · Docker Compose · GitHub Actions + pytest + ruff.

---

## 🔸 5. Code — DAG Airflow (2 min)

**Affiche dans l'IDE** : [airflow/dags/bookshop_pipeline.py](../airflow/dags/bookshop_pipeline.py).

**Tu montres à l'écran :**
1. Les 4 PythonOperator : `create_bookshop_structures`, `ingest_postgres_to_snowflake`, `ensure_dbt_profile`, `dbt_build`.
2. La chaîne de dépendances en bas du fichier : `create >> ingest >> profile >> build`.
3. Les `logger.info()` → observabilité.

**Tu dis :**
> « J'ai choisi quatre tâches Python plutôt que des opérateurs natifs, pour garder la logique visible, testable et traçable via les logs Airflow. »

---

## 🔸 6. Code — Modèles dbt (1,5 min)

**Affiche dans l'IDE** : [app/dbt_bookshop/models/](../app/dbt_bookshop/models/).

**Tu ouvres rapidement :**
- `staging/stg_ventes.sql` — nettoyage / typage.
- `warehouse/fact_ventes.sql` — jointure dim/fact.
- `marts/obt_sales.sql` — dénormalisation finale.

**Tu montres aussi :** `app/dbt_bookshop/macros/generate_schema_name.sql` (la macro qui évite le préfixe `RAW_` sur les schémas dbt).

**Tu dis :**
> « Chaque modèle a des tests dbt (`not_null`, `unique`, `relationships`) qui tournent automatiquement à chaque build — c'est la garantie qualité. »

---

# 🎬 DÉMO LIVE (6-8 min)

À partir d'ici, bascule plein écran sur le navigateur (`F11` ou `⌘+Ctrl+F`).

## 🔹 Démo · étape 1 — Source Postgres (1 min)

**Où :** terminal.
**Commande à taper :**
```bash
docker compose exec -T postgres psql -U bookshop -d bookshop_source -c "
  SELECT 'customers' AS t, COUNT(*) FROM customers UNION ALL
  SELECT 'factures',  COUNT(*) FROM factures  UNION ALL
  SELECT 'ventes',    COUNT(*) FROM ventes;"
```

**Attendu :** 4 customers, 4 factures, 8 ventes.

**Tu dis :**
> « Voici la source : une base transactionnelle PostgreSQL avec 5 tables et une poignée de lignes de démo. »

---

## 🔹 Démo · étape 2 — Injection de données (1 min)

**Où :** même terminal.
**Commande :**
```bash
python3 scripts/seed_demo.py --customers 50 --factures 200
```

**Attendu (sortie console) :**
```
Inserted: 50 customers, 200 factures, ~500 ventes.
```

**Tu dis :**
> « J'injecte 50 clients et 200 factures supplémentaires via Faker — données fictives mais réalistes. »

Re-vérifier le COUNT (optionnel) :
```bash
docker compose exec -T postgres psql -U bookshop -d bookshop_source -c "SELECT COUNT(*) FROM ventes;"
```

---

## 🔹 Démo · étape 3 — Airflow UI (2 min)

**Bascule :** onglet navigateur **Airflow** (`⌘+1`) — `http://localhost:8080`.

**Ce que tu fais :**
1. Page d'accueil → clic sur **`bookshop_pipeline`**.
2. Onglet **Graph** → les 4 tâches en ligne.
3. Clic sur le bouton **▶ (Trigger DAG)** en haut à droite.
4. Attendre ~10 s, les tâches passent du blanc au vert une à une.
5. Clic sur la tâche `dbt_build` → **Log** → montrer les `OK` de dbt.

**Tu dis :**
> « Airflow orchestre les 4 étapes. Chaque tâche a ses logs, ses retries automatiques et une vue Graph qui rend le pipeline lisible. Le run complet prend environ 35 secondes. »

---

## 🔹 Démo · étape 4 — Snowsight (2 min)

**Bascule :** onglet **Snowsight** (`⌘+3`).

**Panneau gauche :** `Data → Databases → BOOKSHOP`.

**Ce que tu montres :**
1. L'arborescence **RAW / STAGGING / WAREHOUSE / MARTS** — les 4 couches.
2. Déplie `MARTS` → `OBT_SALES` → clic droit → **Preview data** → plusieurs centaines de lignes.
3. Bascule sur **Projects → Worksheets → demo_soutenance** (préparé avant).

**Tu lances (⌘+Return ligne par ligne) :**
```sql
USE DATABASE BOOKSHOP;

-- KPI business
SELECT SUM(TOTAL_AMOUNT) AS ca_total,
       SUM(TOTAL_PAID)   AS encaisse,
       ROUND(100 * SUM(TOTAL_PAID) / SUM(TOTAL_AMOUNT), 1) AS taux_reco_pct
FROM WAREHOUSE.FACT_FACTURES;

-- Top 5 livres
SELECT BOOK_INTITULE, SUM(QTE) AS qte_vendue
FROM MARTS.OBT_SALES
GROUP BY BOOK_INTITULE
ORDER BY qte_vendue DESC
LIMIT 5;
```

**Tu dis :**
> « Les données nouvellement injectées sont déjà dans Snowflake, transformées en modèle étoile, et disponibles dans la couche MARTS que consomme le dashboard. »

**Astuce visuelle :** sur le 2e résultat, clic sur **Chart** → choix `Bar` → graphe instantané.

---

## 🔹 Démo · étape 5 — Streamlit (1,5 min)

**Bascule :** onglet **Streamlit** (`⌘+2`) — `http://localhost:8501`.

**Ce que tu fais :**
1. Menu `⋮` (haut droite) → **Rerun** (ou touche `R`) → force le refresh cache.
2. Les 4 KPI en haut se mettent à jour (Ventes, Livres, Clients, Payé).
3. Scroll : histogramme CA par mois, camembert par livre, barres par client.
4. Bas de page : aperçu tabulaire de `OBT_SALES`.

**Tu dis :**
> « Le dashboard Streamlit se connecte directement à la couche MARTS de Snowflake, avec un cache de 5 minutes, des retries exponentiels et une gestion d'erreur propre. Un utilisateur métier n'a jamais besoin d'écrire une ligne de SQL. »

---

# 🏁 FIN DE DÉMO

Bascule vers le PowerPoint pour conclure.

## 🔸 7. Tests & CI (1 min)

**Affiche :** slide 10.

**Tu peux montrer (optionnel, si tu as le temps) :**
- Onglet GitHub `Actions` (`⌘+4`) → pipeline CI vert.
- Dans l'IDE : [tests/test_dag.py](../tests/test_dag.py) — les tests d'intégrité du DAG.

**Tu dis :**
> « À chaque push, GitHub Actions lance ruff, pytest et `dbt parse`. Échec = merge bloqué. »

---

## 🔸 8. Bilan (1 min)

**Affiche :** slide 12.

**Points clés :**
- ~800 lignes de code (Python + SQL + YAML).
- 4 schémas Snowflake, 14 modèles dbt.
- 35 secondes par run complet.
- Reproductible (`make up`), testé, documenté.

---

## 🔸 9. Perspectives (30 s)

**Affiche :** slide 13.

**Tu énumères :**
- CDC avec Debezium / Snowpipe Streaming (remplacer truncate/insert).
- Alerting sur échec DAG (Sentry, Slack).
- Auth Snowflake par clé RSA + secrets manager.
- Airflow managé (MWAA / Astronomer).

---

## 🔸 10. Remerciements (15 s)

**Affiche :** slide 14.

**Tu dis :**
> « Merci pour votre attention. Le code est sur GitHub. Je suis preneur de vos questions. »

---

# 🆘 Plan B — Si ça casse en direct

| Problème | Commande de secours |
|---|---|
| Airflow ne répond pas | `docker compose restart airflow-webserver` puis 30 s d'attente |
| Streamlit cache figé | `docker compose restart streamlit` |
| DAG en erreur | bascule sur le PDF slide 11 et explique ce qui aurait dû se passer |
| Snowsight timeout | bascule sur les captures d'écran dans `docs/screenshots/` (à préparer avant) |
| Postgres port 5432 occupé | déjà sur 5433 dans `.env` — vérifier avec `lsof -i :5433` |
| Tout est cassé | termine sur le PowerPoint — le fond compte plus que la démo |

---

# 📋 Checklist 5 minutes avant l'oral

- [ ] `docker compose ps` → 4 conteneurs running
- [ ] DAG déjà tourné une fois avec succès (Graph vert)
- [ ] Worksheet Snowsight `demo_soutenance` ouvert
- [ ] Dashboard Streamlit déjà chargé (cache chaud)
- [ ] 4 onglets navigateur dans l'ordre (`⌘+1/2/3/4`)
- [ ] Terminal ouvert dans `/Users/msdev224/Desktop/big_data`
- [ ] Mode "Ne pas déranger" Mac activé
- [ ] Bluetooth désactivé (évite notifications AirPods)
- [ ] Dock masqué (`⌘+Option+D`)
- [ ] PDF de la présentation ouvert en arrière-plan
- [ ] Bouteille d'eau à portée

Bonne soutenance ! 🎓
