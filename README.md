# 📚 Projet Big Data M2 — Bookshop

Pipeline data complet d'une librairie : **ingestion → entrepôt cloud → transformations → visualisation**, orchestré automatiquement.

```
PostgreSQL (source locale)
        │
        ▼  Airflow (ingestion)
Snowflake RAW
        │
        ▼  dbt (staging → warehouse → marts)
Snowflake WAREHOUSE / MARTS
        │
        ▼
Streamlit (dashboard)
```

---

## 🧱 Stack

| Couche | Technologie |
|---|---|
| Source transactionnelle | PostgreSQL 15 |
| Data warehouse | Snowflake |
| Transformations SQL | dbt-core 1.9 + dbt-snowflake |
| Orchestration | Apache Airflow 2.10 (LocalExecutor) |
| Dashboard | Streamlit + Plotly |
| Conteneurisation | Docker Compose |

---

## 📁 Arborescence

```
.
├── app/
│   ├── dashboard.py            # Dashboard Streamlit (Plotly)
│   ├── dbt_bookshop/           # Projet dbt (staging / warehouse / marts)
│   └── Dockerfile              # Image Streamlit
├── airflow/
│   ├── dags/bookshop_pipeline.py   # DAG principal
│   ├── Dockerfile              # Image Airflow (+ venv dbt isolé)
│   └── requirements-airflow.txt
├── sql/
│   ├── postgres/               # Schéma + seed de la source
│   └── snowflake/              # DDL RAW + requêtes de vérification
├── scripts/                    # Helpers bash (connexions, dbt, checks)
├── tests/                      # pytest (DAG, dashboard config)
├── docs/                       # Guides, rapport, présentation
├── docker-compose.yml
├── Makefile
└── .env.example
```

---

## 🚀 Démarrage rapide (Docker)

### Prérequis
- Docker Desktop ≥ 24
- Un compte Snowflake trial (voir [docs/setup_snowflake.md](docs/setup_snowflake.md))
- 4 Go de RAM libre

### 1. Préparer `.env`

```bash
cp .env.example .env
```

Puis **générer les secrets** :

```bash
# Fernet key Airflow
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Mots de passe aléatoires
openssl rand -base64 24
```

Reporte les valeurs dans `.env`. Les 3 lignes `SNOWFLAKE_ACCOUNT/USER/PASSWORD` doivent contenir **tes vrais credentials** (voir guide Snowflake).

### 2. Construire + démarrer

```bash
make up
```

Équivalent à :
```bash
docker compose up --build airflow-init
docker compose up --build -d postgres-source airflow-webserver airflow-scheduler streamlit
```

### 3. Créer les connexions Airflow

```bash
make conns
```

Crée `postgres_bookshop` et `snowflake_bookshop` à partir du `.env`.

### 4. Déclencher le pipeline

Interface Airflow : http://localhost:8080
- User : `admin`
- Password : celui défini dans `.env` (`AIRFLOW_ADMIN_PASSWORD`)

Active le DAG `bookshop_pipeline` (toggle) puis clique ▶️ **Trigger DAG**.

Ou en CLI :
```bash
docker compose exec airflow-webserver airflow dags trigger bookshop_pipeline
```

### 5. Voir le dashboard

http://localhost:8501

---

## 📘 Guides détaillés

| Guide | Contenu |
|---|---|
| [docs/setup_snowflake.md](docs/setup_snowflake.md) | Créer un compte Snowflake trial, récupérer l'account identifier, tester la connexion |
| [docs/setup_local.md](docs/setup_local.md) | Lancement sans Docker (venv + Postgres local + dbt CLI) |
| [docs/demo_execution.md](docs/demo_execution.md) | Déroulé complet d'une exécution de démo |
| [docs/data_dictionary.md](docs/data_dictionary.md) | Dictionnaire des tables RAW / WAREHOUSE / MARTS |
| [docs/hypotheses_modele.md](docs/hypotheses_modele.md) | Hypothèses sur le schéma source |
| [docs/architecture.mmd](docs/architecture.mmd) | Diagramme d'architecture (Mermaid) |
| [docs/rapport_projet.md](docs/rapport_projet.md) | Rapport académique complet |

---

## 🔄 Flux du DAG `bookshop_pipeline`

```
create_bookshop_structures  →  ingest_postgres_to_snowflake  →  ensure_dbt_profile  →  dbt_build
         │                              │                             │                    │
         │                              │                             │                    └─ dbt build (staging → warehouse → marts)
         │                              │                             └─ copie profiles.yml.example si besoin
         │                              └─ truncate RAW + insert lignes Postgres
         └─ crée DB, schemas, tables RAW
```

---

## 🛠️ Commandes utiles (Makefile)

| Commande | Effet |
|---|---|
| `make check` | Vérifications rapides (syntaxe) |
| `make up` | Build + démarre tous les services |
| `make init` | Rejoue uniquement l'init Airflow |
| `make conns` | Crée les connexions Airflow |
| `make down` | Stoppe les services (garde les volumes) |
| `make reset-demo` | Détruit **tout** (volumes inclus) et redémarre à zéro |
| `make logs` | Tail des logs des services principaux |
| `make dbt` | Lance `dbt debug` + `dbt build` en local |
| `make dashboard` | Lance Streamlit en local |

---

## 🧪 Tests & CI

```bash
pytest                              # tests (DAG, dashboard config)
ruff check app airflow/dags tests   # lint
```

Le workflow [.github/workflows/ci.yml](.github/workflows/ci.yml) exécute lint + pytest + `dbt parse` sur chaque push et PR.

---

## 🩺 Dépannage

<details>
<summary><b>Airflow refuse de démarrer / connexions illisibles</b></summary>

`AIRFLOW__CORE__FERNET_KEY` est vide ou invalide dans `.env`. Génère :
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
</details>

<details>
<summary><b>Port 5432 déjà utilisé</b></summary>

Un autre Postgres tourne sur ton poste. Change `POSTGRES_PORT=5433` dans `.env`.
</details>

<details>
<summary><b>Dashboard : <code>OperationalError 250001</code> Snowflake</b></summary>

Connexion instable. Augmente dans `.env` :
```env
SNOWFLAKE_LOGIN_TIMEOUT=60
SNOWFLAKE_NETWORK_TIMEOUT=120
SNOWFLAKE_MAX_RETRIES=5
```
</details>

<details>
<summary><b>Le DAG n'apparaît pas dans l'UI</b></summary>

Vérifie que le volume `./airflow/dags` est monté et que le fichier compile :
```bash
docker compose exec airflow-scheduler python -c "import bookshop_pipeline"
```
Et regarde les logs : `docker compose logs airflow-scheduler | tail`.
</details>

<details>
<summary><b>Erreur dbt <code>Profile bookshop not found</code></b></summary>

Le DAG recopie `profiles.yml.example` automatiquement. En local il faut le faire manuellement :
```bash
cp app/dbt_bookshop/profiles.yml.example app/dbt_bookshop/profiles.yml
```
</details>

<details>
<summary><b>Les connexions Airflow disparaissent après <code>make reset-demo</code></b></summary>

C'est attendu (volumes détruits). Relance `make conns`.
</details>

<details>
<summary><b>Conflit de dépendances pip pendant <code>make up</code></b></summary>

Le Dockerfile Airflow utilise les **constraints officielles Airflow** + un **venv isolé pour dbt** pour éviter les conflits `protobuf` / `pandas`. Si tu modifies `requirements-airflow.txt`, garde ce découpage.
</details>

---

## 🔐 Sécurité

- `.env` est dans `.gitignore` → **ne jamais commiter**
- Les mots de passe par défaut de `.env.example` sont des placeholders `change-me`
- La Fernet key Airflow est **obligatoire** et doit être unique par environnement
- Pour la prod Snowflake, utiliser **key-pair auth** plutôt qu'un mot de passe (voir [docs/setup_snowflake.md](docs/setup_snowflake.md) §Avancé)

---

## 📜 Licence / Auteur

Projet académique M2 Big Data — libre d'usage pédagogique.
