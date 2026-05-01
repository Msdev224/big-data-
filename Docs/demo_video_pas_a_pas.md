# Demo video pas a pas

## Objectif

Ce guide vous dit exactement :

- quoi lancer avant la video
- quelle fenetre ouvrir
- ou cliquer
- quoi montrer
- dans quel ordre

L'idee est de faire une demo fluide, sans chercher les fenetres pendant l'enregistrement.

## 1. Preparation avant d'enregistrer

Avant de commencer la capture video, faites tout ceci.

### 1.1 Ouvrir le terminal dans le projet

Dans votre terminal :

```bash
cd "/Users/msdev224/Desktop/big data"
```

### 1.2 Verifier que le fichier `.env` est pret

- Ouvrir le dossier du projet
- Ouvrir le fichier `.env`
- Verifier que vos informations Snowflake sont remplies

Ne montrez pas votre mot de passe a l'ecran pendant la video.

### 1.3 Demarrer les services

Dans le terminal, tapez :

```bash
make up
```

Si `make` ne marche pas :

```bash
docker compose up --build airflow-init
docker compose up --build -d postgres-source airflow-webserver airflow-scheduler streamlit
```

### 1.4 Creer les connexions Airflow

Dans le terminal :

```bash
make conns
```

Ou :

```bash
docker compose exec airflow-webserver bash /opt/airflow/project/scripts/create_airflow_connections.sh
```

### 1.5 Verifier les URL

Ouvrir dans le navigateur :

- Airflow : `http://localhost:8080`
- Streamlit : `http://localhost:8501`

### 1.6 Se connecter a Airflow

Sur la page Airflow :

- cliquer dans le champ `Username`
- taper `admin`
- cliquer dans le champ `Password`
- taper `admin`
- cliquer sur `Sign In`

### 1.7 Lancer le DAG avant l'enregistrement

Dans Airflow :

- trouver la ligne `bookshop_pipeline`
- si le DAG est desactive, cliquer sur le bouton pour l'activer
- cliquer sur le nom `bookshop_pipeline`
- cliquer sur l'onglet `Graph`
- revenir en haut si besoin
- cliquer sur le bouton `Trigger DAG`

Attendre que toutes les taches soient au vert.

### 1.8 Preparer les fenetres pour la video

Mettez les fenetres dans cet ordre :

1. VS Code ou votre editeur
2. terminal
3. Snowflake
4. Airflow
5. Streamlit

Gardez deja ouverts :

- [README.md](/Users/msdev224/Desktop/big%20data/README.md#L1)
- [sql/postgres/01_schema.sql](/Users/msdev224/Desktop/big%20data/sql/postgres/01_schema.sql#L1)
- [sql/postgres/02_seed.sql](/Users/msdev224/Desktop/big%20data/sql/postgres/02_seed.sql#L1)
- [app/dbt_bookshop/models/staging/stg_ventes.sql](/Users/msdev224/Desktop/big%20data/app/dbt_bookshop/models/staging/stg_ventes.sql#L1)
- [app/dbt_bookshop/models/warehouse/fact_ventes.sql](/Users/msdev224/Desktop/big%20data/app/dbt_bookshop/models/warehouse/fact_ventes.sql#L1)
- [app/dbt_bookshop/models/marts/obt_sales.sql](/Users/msdev224/Desktop/big%20data/app/dbt_bookshop/models/marts/obt_sales.sql#L1)
- [airflow/dags/bookshop_pipeline.py](/Users/msdev224/Desktop/big%20data/airflow/dags/bookshop_pipeline.py#L1)
- [sql/snowflake/03_verification_queries.sql](/Users/msdev224/Desktop/big%20data/sql/snowflake/03_verification_queries.sql#L1)

## 2. Debut de la video

### 2.1 Montrer le projet

**Fenetre**

- editeur de code

**Ou cliquer**

- cliquer sur l'onglet `README.md`

**Quoi montrer**

- le titre du projet
- la stack choisie

**A faire**

- rester 3 secondes sur le haut de la page

### 2.2 Montrer l'arborescence

**Fenetre**

- editeur de code

**Ou cliquer**

- dans l'explorateur de fichiers a gauche

**Quoi montrer**

- `sql`
- `airflow`
- `app`
- `docs`

**A faire**

- ouvrir `sql`
- ouvrir `airflow`
- ouvrir `app`

## 3. Montrer la base source PostgreSQL

### 3.1 Montrer le schema source

**Fenetre**

- editeur de code

**Ou cliquer**

- cliquer sur `sql/postgres/01_schema.sql`

**Quoi montrer**

- les tables `category`, `books`, `customers`, `factures`, `ventes`

**A faire**

- descendre lentement avec la molette
- faire une pause sur chaque `CREATE TABLE`

### 3.2 Montrer les donnees d'exemple

**Fenetre**

- editeur de code

**Ou cliquer**

- cliquer sur `sql/postgres/02_seed.sql`

**Quoi montrer**

- les `INSERT INTO`
- les exemples de livres, clients, factures et ventes

**A faire**

- descendre doucement

### 3.3 Montrer dans le terminal que la base est lancee

**Fenetre**

- terminal

**Ou cliquer**

- revenir sur le terminal

**Commande a taper**

```bash
docker compose ps
```

**Quoi montrer**

- que `postgres-source`, `airflow-webserver`, `airflow-scheduler` et `streamlit` tournent

## 4. Montrer Snowflake

### 4.1 Ouvrir Snowflake

**Fenetre**

- navigateur sur Snowflake

**Ou cliquer**

- dans le menu de gauche, ouvrir la partie `Data`
- ouvrir la base `BOOKSHOP`

**Quoi montrer**

- les schemas `RAW`, `STAGGING`, `WAREHOUSE`, `MARTS`

### 4.2 Montrer les tables RAW

**Ou cliquer**

- cliquer sur `RAW`

**Quoi montrer**

- `CATEGORY`
- `BOOKS`
- `CUSTOMERS`
- `FACTURES`
- `VENTES`

### 4.3 Montrer une table RAW

**Ou cliquer**

- cliquer sur `VENTES`
- cliquer sur `Preview` si disponible

**Quoi montrer**

- les colonnes
- le champ `DATE_EDIT`

## 5. Montrer dbt

### 5.1 Montrer le projet dbt

**Fenetre**

- editeur de code

**Ou cliquer**

- dans l'explorateur, ouvrir `app/dbt_bookshop/models`

**Quoi montrer**

- `staging`
- `warehouse`
- `marts`

### 5.2 Montrer la transformation STAGGING

**Ou cliquer**

- cliquer sur `app/dbt_bookshop/models/staging/stg_ventes.sql`

**Quoi montrer**

- la conversion `to_date(date_edit, 'YYYYMMDD')`

### 5.3 Montrer la transformation WAREHOUSE

**Ou cliquer**

- cliquer sur `app/dbt_bookshop/models/warehouse/fact_ventes.sql`

**Quoi montrer**

- `annees`
- `mois`
- `jour`

### 5.4 Montrer la table finale MARTS

**Ou cliquer**

- cliquer sur `app/dbt_bookshop/models/marts/obt_sales.sql`

**Quoi montrer**

- les jointures entre ventes, factures, livres, categories et clients

## 6. Montrer Airflow

### 6.1 Montrer le code du DAG

**Fenetre**

- editeur de code

**Ou cliquer**

- cliquer sur `airflow/dags/bookshop_pipeline.py`

**Quoi montrer**

- les trois etapes principales

### 6.2 Montrer le DAG dans l'interface

**Fenetre**

- navigateur sur Airflow

**Ou cliquer**

- cliquer sur `DAGs`
- cliquer sur `bookshop_pipeline`
- cliquer sur `Graph`

**Quoi montrer**

- `create_bookshop_structures`
- `ingest_postgres_to_snowflake`
- `dbt_build`

### 6.3 Montrer l'execution reussie

**Ou cliquer**

- cliquer sur une tache verte si besoin
- cliquer sur `Task Instance Details` si vous voulez

**Quoi montrer**

- que toutes les taches sont bien au vert

## 7. Montrer les verifications Snowflake

### 7.1 Ouvrir les requetes de verification

**Fenetre**

- editeur de code

**Ou cliquer**

- cliquer sur `sql/snowflake/03_verification_queries.sql`

**Quoi montrer**

- les requetes de controle

### 7.2 Executer les verifications dans Snowflake

**Fenetre**

- Snowflake

**Ou cliquer**

- ouvrir un worksheet SQL
- coller ou taper quelques requetes

**Requetes a lancer**

```sql
show tables in schema BOOKSHOP.RAW;
show tables in schema BOOKSHOP.STAGGING;
show tables in schema BOOKSHOP.WAREHOUSE;
show tables in schema BOOKSHOP.MARTS;
select * from BOOKSHOP.MARTS.OBT_SALES order by vente_id;
```

**Quoi montrer**

- que toutes les couches existent
- que `OBT_SALES` contient des lignes

## 8. Montrer Streamlit

### 8.1 Ouvrir le dashboard

**Fenetre**

- navigateur sur Streamlit

**Ou cliquer**

- aller sur `http://localhost:8501`

**Quoi montrer**

- le titre du dashboard
- les KPI

### 8.2 Montrer les graphiques

**A faire**

- descendre doucement avec la molette

**Quoi montrer**

- ventes par mois
- repartition des ventes par livre
- montant paye par client

### 8.3 Montrer la table finale

**A faire**

- descendre jusqu'a la table

**Quoi montrer**

- l'aperçu de `MARTS.OBT_SALES`

## 9. Fin de la video

### 9.1 Revenir sur une vue globale

Vous pouvez finir soit sur :

- le dashboard Streamlit
- ou le `README`

### 9.2 Ce qu'il faut montrer a la fin

- la solution est complete
- la chaine part de PostgreSQL
- la donnee arrive dans Snowflake
- dbt transforme
- Airflow orchestre
- Streamlit visualise

## 10. Version ultra simple de l'ordre exact de clics

1. Ouvrir `README.md`
2. Montrer l'arborescence
3. Cliquer sur `sql/postgres/01_schema.sql`
4. Cliquer sur `sql/postgres/02_seed.sql`
5. Aller dans le terminal et taper `docker compose ps`
6. Aller dans Snowflake et ouvrir `BOOKSHOP`
7. Cliquer sur `RAW`
8. Cliquer sur `VENTES`
9. Revenir dans l'editeur
10. Cliquer sur `stg_ventes.sql`
11. Cliquer sur `fact_ventes.sql`
12. Cliquer sur `obt_sales.sql`
13. Cliquer sur `bookshop_pipeline.py`
14. Aller dans Airflow
15. Cliquer sur `bookshop_pipeline`
16. Cliquer sur `Graph`
17. Montrer les taches vertes
18. Aller dans Snowflake
19. Lancer les requetes de verification
20. Montrer `MARTS.OBT_SALES`
21. Aller dans Streamlit
22. Montrer les KPI
23. Descendre sur les graphiques
24. Descendre sur la table finale
25. Finir sur une conclusion

## 11. Astuce importante

Pendant l'enregistrement, ne tapez pas trop de commandes sauf si c'est vraiment utile.

Le mieux est de :

- tout preparer avant
- lancer le pipeline avant la video
- montrer surtout les resultats

La video sera plus propre, plus fluide et plus convaincante.
