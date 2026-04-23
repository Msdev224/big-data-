# 🖥️ Guide d'installation locale (sans Docker)

Ce guide s'adresse à ceux qui préfèrent lancer le projet directement sur
leur machine, sans Docker. Utile pour déboguer ou développer le dashboard
et les modèles dbt.

> ℹ️ **Recommandation** : pour une première exécution, utilise plutôt Docker
> (voir [README.md](../README.md) §Démarrage rapide). Ce mode local demande
> plus d'étapes manuelles.

---

## 1. Prérequis

| Outil | Version | Vérification |
|---|---|---|
| Python | 3.11 | `python3 --version` |
| PostgreSQL | 15 | `psql --version` |
| Compte Snowflake | trial | voir [setup_snowflake.md](setup_snowflake.md) |
| `git` | toute | `git --version` |

Sur macOS :
```bash
brew install python@3.11 postgresql@15
brew services start postgresql@15
```

---

## 2. Environnement Python

```bash
cd big_data
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ `dbt-core 1.9` demande `protobuf>=5`, ce qui entre en conflit avec les
> constraints Airflow. En local, sans Airflow installé, aucun problème.

---

## 3. Base PostgreSQL locale

### Créer l'utilisateur et la base

```bash
createuser -P bookshop          # demande un mot de passe
createdb -O bookshop bookshop_source
```

### Charger le schéma et les données

```bash
psql -U bookshop -d bookshop_source -f sql/postgres/01_schema.sql
psql -U bookshop -d bookshop_source -f sql/postgres/02_seed.sql
```

Vérifier :
```bash
psql -U bookshop -d bookshop_source -c "\dt"
# attendu : books, category, customers, factures, ventes
```

---

## 4. Fichier `.env`

```bash
cp .env.example .env
```

Renseigne :
- `POSTGRES_*` (avec le mot de passe créé à l'étape 3)
- `SNOWFLAKE_*` (voir [setup_snowflake.md](setup_snowflake.md))
- `AIRFLOW__CORE__FERNET_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")`

---

## 5. Préparer Snowflake

Depuis Snowsight, exécute dans l'ordre :
- [sql/snowflake/01_setup_bookshop.sql](../sql/snowflake/01_setup_bookshop.sql)
- [sql/snowflake/02_raw_tables.sql](../sql/snowflake/02_raw_tables.sql)

---

## 6. Configurer dbt

```bash
cp app/dbt_bookshop/profiles.yml.example app/dbt_bookshop/profiles.yml
```

Puis :
```bash
cd app/dbt_bookshop
dbt debug --profiles-dir .
```

Sortie attendue : `All checks passed!`

---

## 7. Ingestion manuelle Postgres → Snowflake

Sans Airflow, tu peux ingérer manuellement avec un script Python minimal :

```python
# scripts/ingest_manual.py
import os
import psycopg2
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

TABLES = {
    "CATEGORY": ["ID", "CODE", "INTITULE"],
    "BOOKS": ["ID", "CATEGORY_ID", "CODE", "INTITULE", "ISBN_10", "ISBN_13", "PRIX_CATALOGUE"],
    "CUSTOMERS": ["ID", "CODE", "FIRST_NAME", "LAST_NAME", "EMAIL", "CITY", "COUNTRY"],
    "FACTURES": ["ID", "CUSTOMER_ID", "CODE", "QTE_TOTALE", "TOTAL_AMOUNT", "TOTAL_PAID", "DATE_EDIT"],
    "VENTES": ["ID", "FACTURE_ID", "BOOK_ID", "PU", "QTE", "DATE_EDIT"],
}

pg = psycopg2.connect(
    host=os.environ["POSTGRES_HOST"],
    port=os.environ["POSTGRES_PORT"],
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)
sf = snowflake.connector.connect(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    user=os.environ["SNOWFLAKE_USER"],
    password=os.environ["SNOWFLAKE_PASSWORD"],
    warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
    database=os.environ["SNOWFLAKE_DATABASE"],
    role=os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
)

for table, cols in TABLES.items():
    with pg.cursor() as c:
        c.execute(f"select {','.join(col.lower() for col in cols)} from {table.lower()}")
        rows = c.fetchall()
    if not rows:
        continue
    placeholders = ",".join(["%s"] * len(cols))
    with sf.cursor() as c:
        c.execute(f"truncate table if exists BOOKSHOP.RAW.{table}")
        c.executemany(
            f"insert into BOOKSHOP.RAW.{table} ({','.join(cols)}) values ({placeholders})",
            rows,
        )
    print(f"✓ {table}: {len(rows)} lignes")

sf.commit()
pg.close()
sf.close()
```

Lancer :
```bash
python scripts/ingest_manual.py
```

---

## 8. Lancer dbt

```bash
cd app/dbt_bookshop
dbt build --profiles-dir .
```

Build = run + test. Tu obtiens :
- Modèles `STAGING.*`, `WAREHOUSE.*`, `MARTS.OBT_SALES`
- Tests automatiques (unicité, non-null, relations)

---

## 9. Lancer le dashboard

```bash
streamlit run app/dashboard.py
```

Ouvre http://localhost:8501.

---

## 10. (Optionnel) Airflow local

Installer Airflow localement est fastidieux à cause de la matrice de
dépendances. Utilise plutôt Docker pour la partie orchestration :

```bash
docker compose up --build -d airflow-webserver airflow-scheduler
```

Les autres services (Postgres, dbt, Streamlit) peuvent rester en local.

---

## 11. Dépannage local

| Erreur | Solution |
|---|---|
| `psql: could not connect to server` | `brew services start postgresql@15` |
| `FATAL: role "bookshop" does not exist` | Refaire l'étape 3 (`createuser -P bookshop`) |
| `dbt debug` : `database error` | Vérifier `.env` et `profiles.yml`, `SELECT CURRENT_ACCOUNT()` dans Snowsight |
| Streamlit : `ModuleNotFoundError: snowflake` | Activer le venv : `source .venv/bin/activate` |
| `dbt build` : `Compilation Error in rpc request` | `dbt clean && dbt deps && dbt build` |
