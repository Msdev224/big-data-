# 📚 Bookshop Big Data

Pipeline Big Data de bout en bout pour une librairie : ingestion depuis PostgreSQL,
entrepôt analytique Snowflake modélisé avec dbt, dashboard Streamlit, le tout
orchestré par Airflow et déployable en une commande avec Docker Compose.

> **Projet académique — Master 2 Big Data · Mamadou Saidou Bah · Avril 2026**

---

## 🎯 Ce que fait le projet

```
┌──────────────┐   ┌──────────┐   ┌────────────────────────────────────┐   ┌────────────┐
│ PostgreSQL   │──▶│ Airflow  │──▶│ Snowflake                          │──▶│ Streamlit  │
│ (OLTP, 5 tb) │   │ (4 tasks)│   │ RAW → STAGGING → WAREHOUSE → MARTS │   │ (Plotly)   │
└──────────────┘   └──────────┘   └────────────────────────────────────┘   └────────────┘
                                              ▲
                                              │
                                          dbt build
                                     (modèles + tests)
```

- **Source** PostgreSQL 15 (5 tables transactionnelles).
- **Orchestration** Apache Airflow 2.10 (1 DAG, 4 tâches).
- **Entrepôt** Snowflake (trial AWS eu-west-3), 4 schémas.
- **Transformations** dbt-core 1.9 + dbt-snowflake 1.9, 14 modèles, tests `not_null` / `unique` / `relationships`.
- **Restitution** Streamlit + Plotly avec cache, retries et gestion des timeouts.
- **Qualité** ruff + pytest + `dbt parse` via GitHub Actions.

---

## 🚀 Démarrage rapide

### Prérequis

| Outil | Version mini | Vérif |
|---|---|---|
| Docker Desktop | 24+ | `docker --version` |
| Docker Compose | v2 | `docker compose version` |
| Python (optionnel, hôte) | 3.11 | `python3 --version` |
| Compte Snowflake | trial 30 jours | [signup.snowflake.com](https://signup.snowflake.com/) |

### Configuration en 3 étapes

```bash
# 1. Cloner
git clone https://github.com/Msdev224/big-data-.git bookshop-bigdata
cd bookshop-bigdata

# 2. Créer le fichier d'env local
cp .env.example .env
# Éditer .env et renseigner les variables SNOWFLAKE_* (cf. docs/setup_snowflake.md)
# Airflow Fernet key à générer avec :
#   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# 3. Démarrer la stack
make up
```

`make up` lance **4 conteneurs** : `postgres-source`, `airflow-webserver`, `airflow-scheduler`, `streamlit`.

### Accès aux UIs

| Service | URL | Identifiants |
|---|---|---|
| Airflow | http://localhost:8080 | `admin` / `AIRFLOW_ADMIN_PASSWORD` du `.env` |
| Streamlit | http://localhost:8501 | — |
| Snowsight | https://app.snowflake.com/ | User / Password Snowflake |

### Premier run

1. UI Airflow → DAG `bookshop_pipeline` → **▶ Trigger DAG**.
2. Les 4 tâches passent au vert en ~35 s.
3. Streamlit charge automatiquement les KPI depuis `BOOKSHOP.MARTS.OBT_SALES`.

---

## 🗂 Arborescence

```
.
├── airflow/
│   ├── dags/bookshop_pipeline.py       # DAG unique, 4 PythonOperators
│   ├── Dockerfile                      # Airflow + dbt dans venv isolé
│   └── requirements-airflow.txt
├── app/
│   ├── config.py                       # Config Snowflake (timeouts, retries)
│   ├── dashboard.py                    # Streamlit + Plotly
│   ├── dbt_bookshop/                   # Projet dbt
│   │   ├── models/
│   │   │   ├── staging/                # stg_* (nettoyage)
│   │   │   ├── warehouse/              # dim_*, fact_* (étoile)
│   │   │   └── marts/                  # obt_sales (dénormalisée)
│   │   ├── macros/generate_schema_name.sql
│   │   └── profiles.yml.example
│   └── Dockerfile
├── sql/
│   ├── postgres/                       # 01_schema.sql, 02_seed.sql (auto-init)
│   └── snowflake/                      # 01_setup, 02_raw_tables, 03_verif
├── scripts/
│   ├── create_airflow_connections.sh   # Conn postgres_bookshop + snowflake_bookshop
│   ├── seed_demo.py                    # Faker fr_FR — inject N clients/factures
│   └── run_dbt.sh / run_dashboard.sh   # Scripts utilitaires
├── tests/
│   ├── test_dag.py                     # DAG integrity + RAW_TABLES
│   └── test_dashboard_config.py        # Timeouts/retries defaults
├── docker-compose.yml
├── Makefile                            # up, down, logs, dbt, reset-demo
├── pyproject.toml                      # Config pytest + ruff
├── requirements.txt
└── .github/workflows/ci.yml            # lint + pytest + dbt parse
```

---

## 🛠 Commandes Makefile

```bash
make up            # Démarre toute la stack
make down          # Arrête sans supprimer les volumes
make reset-demo    # Purge tout (⚠ volumes) et recrée
make logs          # Tail des logs des 4 services
make conns         # (Re)crée les Airflow connections postgres/snowflake
make dbt           # Lance dbt build hors Airflow (debug rapide)
make dashboard     # Lance Streamlit hors Docker (si Python local prêt)
make check         # Vérifie l'environnement (docker, .env, ports)
```

---

## 📊 Modèle de données

### Source PostgreSQL (`bookshop_source`)

| Table | Rôle |
|---|---|
| `category` | Catégories de livres |
| `books` | Catalogue (ISBN, prix) |
| `customers` | Clients (nom, email, ville, pays) |
| `factures` | Entêtes (total, payé, date) |
| `ventes` | Lignes de facture (book_id, qte, pu) |

### Entrepôt Snowflake (`BOOKSHOP`)

| Schéma | Contenu | Type |
|---|---|---|
| `RAW` | Copie brute des 5 tables Postgres | Tables |
| `STAGGING` | `stg_*` nettoyage + typage | Vues |
| `WAREHOUSE` | `dim_*` + `fact_*` + agrégats temporels | Tables |
| `MARTS` | `obt_sales` dénormalisée pour le dashboard | Table |

> **Note** : le nommage `STAGGING` (double G) est conservé tel quel par choix projet.
> La macro `generate_schema_name` garantit l'absence de préfixe `RAW_`.

---

## 🎬 Démo avancée — injection de données

Pendant la soutenance, enrichir la source en live pour montrer la chaîne réagir :

```bash
# 50 clients + 200 factures + ~500 ventes via Faker (locale fr_FR)
python3 scripts/seed_demo.py --customers 50 --factures 200

# Re-trigger le pipeline
docker compose exec -T airflow-webserver airflow dags trigger bookshop_pipeline

# Rafraîchir le dashboard (touche R) → les KPI bougent
```

Runbook complet dans `docs/demo_runbook.md` (non versionné).

---

## ✅ Tests & CI

```bash
ruff check app airflow/dags tests
pytest
cd app/dbt_bookshop && dbt parse --profiles-dir .
```

GitHub Actions exécute automatiquement ces 3 étapes sur chaque push / PR :
[Actions](https://github.com/Msdev224/big-data-/actions).

---

## 🛡 Sécurité

- `.env` est **gitignoré** — aucun secret n'atterrit sur GitHub.
- `.env.example` ne contient que des valeurs `change-me`.
- Fernet key Airflow obligatoire → chiffrement des connections/variables.
- Mot de passe admin Airflow aléatoire (à générer à la première install).
- Auth Snowflake par mot de passe en dev — migration clé RSA prévue pour la prod.

---

## 🩺 Dépannage express

<details>
<summary><b>Port 5432 déjà occupé</b></summary>

Postgres local sur l'hôte. Le projet utilise déjà `5433` côté hôte — vérifier `.env`
et `lsof -i :5433`. Si conflit persistant : changer `POSTGRES_PORT` dans `.env`.
</details>

<details>
<summary><b>DAG import error / red triangle</b></summary>

```bash
docker compose exec airflow-scheduler airflow dags list-import-errors
docker compose logs --tail=80 airflow-scheduler
```
</details>

<details>
<summary><b>Dashboard : "BOOKSHOP.MARTS.OBT_SALES does not exist"</b></summary>

dbt a créé `RAW_MARTS` au lieu de `MARTS`. Vérifier que
`app/dbt_bookshop/macros/generate_schema_name.sql` existe et contient la macro
de surcharge. Relancer le DAG.
</details>

<details>
<summary><b>Snowflake OCSP / timeout</b></summary>

Augmenter les timeouts dans `.env` :
```
SNOWFLAKE_LOGIN_TIMEOUT=60
SNOWFLAKE_NETWORK_TIMEOUT=120
SNOWFLAKE_MAX_RETRIES=5
```
</details>

<details>
<summary><b>Snowsight : "This session does not have a current database"</b></summary>

Ajouter en haut du worksheet :
```sql
USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE BOOKSHOP;
```
</details>

---

## 🧭 Perspectives

- **CDC** avec Debezium ou Snowpipe Streaming (remplacer le `TRUNCATE + INSERT`).
- **Alerting** : hooks `on_failure_callback` vers Sentry / Slack.
- **Sécurité** : auth Snowflake par clé RSA, secrets via Vault / AWS SSM.
- **Catalog** : `dbt docs generate` + publication Datahub / OpenMetadata.
- **Infra** : migration vers MWAA / Astronomer pour la HA.

---

## 📄 Licence & auteur

Projet académique non distribué — **Mamadou Saidou Bah**, Master 2 Big Data, 2026.
