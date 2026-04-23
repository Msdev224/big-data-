# Sequence de demo

## 1. Montrer le code source

- ouvrir l'arborescence du projet
- expliquer les dossiers `sql`, `airflow`, `app`, `docs`

## 2. Montrer PostgreSQL

- afficher les tables source
- expliquer le role de la base locale dans l'ingestion

## 3. Montrer Snowflake

- ouvrir la base `BOOKSHOP`
- montrer les schemas `RAW`, `STAGGING`, `WAREHOUSE`, `MARTS`

## 4. Montrer Airflow

- ouvrir le DAG `bookshop_pipeline`
- expliquer les trois etapes principales :
  - creation des structures
  - ingestion RAW
  - execution dbt

## 5. Montrer dbt

- afficher un modele `stg_ventes`
- afficher `fact_ventes`
- afficher `obt_sales`

## 6. Montrer les verifications

- lancer quelques requetes de `03_verification_queries.sql`
- confirmer les nombres de tables et la presence de donnees

## 7. Montrer le dashboard

- KPI
- ventes par mois
- top livres
- paiements clients

## 8. Conclure

- rappeler que la chaine complete va de la source locale jusqu'a la table MARTS
- insister sur l'automatisation et la visualisation
