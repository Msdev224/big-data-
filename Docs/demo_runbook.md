# Runbook démo — injection de données & rafraîchissement pipeline

Procédure complète pour enrichir la source PostgreSQL, rejouer le pipeline,
puis rafraîchir le dashboard — à dérouler tel quel pendant la soutenance.

---

## 0. Pré-requis (une seule fois)

Les stack doit être démarrée (`make up` ou `docker compose up -d`) et le DAG
`bookshop_pipeline` doit déjà avoir tourné au moins une fois avec succès.

Installer les deux libs utilisées par le script (hôte, pas Docker) :

```bash
cd /Users/msdev224/Desktop/big_data
python3 -m pip install faker psycopg2-binary python-dotenv
```

---

## 1. Vérifier l'état initial

```bash
# Combien de lignes actuellement côté source ?
docker compose exec -T postgres psql -U bookshop -d bookshop_source -c "
  SELECT 'customers' AS t, COUNT(*) FROM customers UNION ALL
  SELECT 'factures',  COUNT(*) FROM factures  UNION ALL
  SELECT 'ventes',    COUNT(*) FROM ventes;"
```

Attendu après le seed de base : 4 customers, 4 factures, 8 ventes.

---

## 2. Injecter des données synthétiques (Faker · locale fr_FR)

```bash
# Volume "soutenance" : ~50 clients, 200 factures, ~500 ventes
python3 scripts/seed_demo.py --customers 50 --factures 200
```

Variantes selon l'effet recherché :

| Objectif                     | Commande                                           |
|------------------------------|----------------------------------------------------|
| Petit boost visuel           | `python3 scripts/seed_demo.py --customers 20 --factures 50`   |
| Démo standard                | `python3 scripts/seed_demo.py --customers 50 --factures 200`  |
| Montrer la scalabilité       | `python3 scripts/seed_demo.py --customers 500 --factures 2000`|
| Ajouter un 2e batch en live  | relancer la même commande — les IDs s'enchaînent   |

Vérification immédiate côté Postgres :

```bash
docker compose exec -T postgres psql -U bookshop -d bookshop_source -c "
  SELECT COUNT(*) AS customers FROM customers;
  SELECT COUNT(*) AS factures  FROM factures;
  SELECT COUNT(*) AS ventes    FROM ventes;"
```

---

## 3. Re-déclencher le pipeline Airflow

### Option A — via l'UI (démo visuelle, recommandée)

1. Ouvrir <http://localhost:8080> (admin / mot de passe `.env`).
2. Cliquer sur le DAG `bookshop_pipeline`.
3. Bouton **▶ Trigger DAG** (coin haut droit).
4. Observer les 4 tâches passer au vert (~35 s).

### Option B — via la CLI Airflow (plus rapide)

```bash
docker compose exec -T airflow-webserver airflow dags trigger bookshop_pipeline
```

### Vérifier que le run est terminé

```bash
docker compose exec -T airflow-webserver airflow dags list-runs -d bookshop_pipeline | head
```

---

## 4. Vérifier Snowflake

Depuis Snowsight (`BOOKSHOP` > `MARTS` > `OBT_SALES`), ou via SQL :

```sql
USE DATABASE BOOKSHOP;
USE SCHEMA MARTS;

SELECT COUNT(*) FROM OBT_SALES;
SELECT SUM(TOTAL_AMOUNT) FROM WAREHOUSE.FACT_FACTURES;
SELECT * FROM OBT_SALES ORDER BY DATE_EDIT DESC LIMIT 20;
```

---

## 5. Rafraîchir le dashboard Streamlit

Le dashboard met en cache 5 min. Deux options :

```bash
# Option rapide : forcer le reload en vidant le cache via redémarrage
docker compose restart streamlit
```

Ou dans le navigateur (<http://localhost:8501>) : menu `⋮` en haut à droite → **Rerun** (touche `R`).

KPI à commenter pendant la démo :

- **Ventes** (lignes) → passe de 8 à plusieurs centaines
- **Clients** → +50
- **Taux de recouvrement** → se stabilise vers ~80 % (ratio pondéré du script)
- L'histogramme CA par mois devient significatif
- Le camembert des ventes par livre équilibre ses 5 parts

---

## 6. Enchaînement "live" (script pour la soutenance)

À projeter en mode split-screen (terminal + navigateur) :

```bash
# T-0 : état initial
docker compose exec -T postgres psql -U bookshop -d bookshop_source -c "SELECT COUNT(*) FROM ventes;"

# T+10s : on injecte
python3 scripts/seed_demo.py --customers 50 --factures 200

# T+15s : on déclenche
docker compose exec -T airflow-webserver airflow dags trigger bookshop_pipeline

# T+50s : on recharge le dashboard (touche R sur Streamlit)
# → les KPI bougent sous les yeux du jury
```

---

## 7. Reset complet (optionnel, après la démo)

Repartir d'un état propre :

```bash
docker compose exec -T postgres psql -U bookshop -d bookshop_source <<'SQL'
  TRUNCATE ventes, factures, customers RESTART IDENTITY CASCADE;
SQL

docker compose exec -T postgres psql -U bookshop -d bookshop_source \
  -f /docker-entrypoint-initdb.d/02_seed.sql

docker compose exec -T airflow-webserver airflow dags trigger bookshop_pipeline
```

Côté Snowflake, le DAG fait `TRUNCATE` sur RAW à chaque run, donc pas d'action
manuelle nécessaire — le prochain trigger réaligne tout.
