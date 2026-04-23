# Rapport de projet - Architecture Big Data Bookshop

## 1. Introduction

Dans le cadre du cours d'Architecture Big Data, ce projet consiste à mettre en place une chaîne
complète de traitement de données pour une structure qui vend des livres. L'objectif principal est
de transformer des données brutes de vente en une table OBT (`One Big Table`) permettant
l'analyse métier.

La solution implémentée s'appuie sur quatre briques principales :

- PostgreSQL comme source locale de données
- Snowflake comme entrepôt de données cloud
- dbt pour les transformations
- Airflow pour l'orchestration

Une couche de visualisation a également été ajoutée avec Streamlit.

## 2. Architecture de la solution

Le pipeline suit les étapes suivantes :

1. Les données sont créées dans une base PostgreSQL locale.
2. Airflow orchestre l'ingestion de ces données dans Snowflake, schéma `RAW`.
3. dbt transforme les données :
   - `RAW -> STAGGING`
   - `STAGGING -> WAREHOUSE`
   - `WAREHOUSE -> MARTS`
4. Streamlit interroge les tables `WAREHOUSE` et `MARTS` pour produire des graphiques.

## 3. Description des données sources

Les tables métiers manipulées sont :

- `category`
- `books`
- `customers`
- `factures`
- `ventes`

Le champ `date_edit` des tables `ventes` et `factures` est stocké au format `YYYYMMDD` dans la
source locale, puis converti en vrai type `DATE` dans `STAGGING`.

## 4. Mise en oeuvre

### 4.1 Base locale PostgreSQL

Le schéma de la base locale a été défini dans `sql/postgres/01_schema.sql` et les données
d'exemple dans `sql/postgres/02_seed.sql`.

Cette étape répond à la partie "Ingestion" demandée dans la touche personnelle :

- création d'une base locale
- alimentation des tables
- préparation de l'ingestion vers Snowflake

### 4.2 Snowflake

Dans Snowflake, une base `BOOKSHOP` est créée avec les schémas suivants :

- `RAW`
- `STAGGING`
- `WAREHOUSE`
- `MARTS`

Le schéma `RAW` contient la copie des tables sources.

### 4.3 Transformations dbt

#### RAW -> STAGGING

Les traitements réalisés sont :

- conversion du champ `date_edit` de `RAW.ventes` vers `STAGGING.stg_ventes`
- conversion du champ `date_edit` de `RAW.factures` vers `STAGGING.stg_factures`
- copie des tables `category`, `books`, `customers` vers leurs équivalents `stg_*`

Résultat : 5 tables commençant par `stg_`.

#### STAGGING -> WAREHOUSE

Les objets produits sont :

- `dim_category`
- `dim_books`
- `dim_customers`
- `fact_ventes`
- `fact_factures`
- `fact_books_annees`
- `fact_books_mois`
- `fact_books_jour`

Les enrichissements principaux sont :

- ajout de `nom = first_name || ' ' || last_name` dans `dim_customers`
- extraction de `annees`, `mois`, `jour` depuis `date_edit` dans les tables de faits
- agrégation des livres vendus par année, mois et jour

#### WAREHOUSE -> MARTS

Une table unique `MARTS.obt_sales` est créée. Elle regroupe :

- les informations de ligne de vente
- les informations de facture
- la catégorie du livre
- les métadonnées du livre
- l'identité du client

Cette table répond directement à l'énoncé de l'OBT finale.

## 5. Orchestration avec Airflow

Le DAG `bookshop_pipeline` exécute les tâches suivantes :

1. Création de la base et des schémas Snowflake
2. Création des tables `RAW`
3. Lecture des données de PostgreSQL
4. Chargement dans Snowflake
5. Lancement de `dbt build`

L'intérêt d'Airflow est de garantir :

- l'automatisation
- l'ordonnancement
- la traçabilité des traitements

## 6. Visualisation

Le dashboard Streamlit met en valeur :

- le nombre de ventes
- le chiffre d'affaires
- les montants payés
- les ventes par mois
- les livres les plus vendus
- les montants payés par client
- un aperçu détaillé de la table `MARTS.obt_sales`

Cette partie répond à la touche personnelle sur la visualisation.

## 7. Difficultés et choix techniques

Le document mentionne Snowflake, dbt et Airflow comme propositions et autorise d'autres outils.
Pour rester au plus proche de l'énoncé, ces trois composants ont été conservés.

Le diagramme source n'étant pas totalement extractible textuellement depuis le PDF, une
modélisation minimale et cohérente a été proposée pour permettre l'exécution complète du projet.

## 8. Conclusion

Ce projet met en oeuvre une architecture décisionnelle moderne, claire et évolutive :

- une zone source locale
- une zone RAW
- une zone STAGGING
- une zone WAREHOUSE
- une zone MARTS

La solution est industrialisable et peut être enrichie plus tard avec :

- davantage de données
- des tests dbt supplémentaires
- des snapshots dbt
- une visualisation plus riche avec filtres et segmentation
