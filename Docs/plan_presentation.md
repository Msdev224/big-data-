# Plan PowerPoint

## Slide 1 - Titre

- Projet Big Data M2
- Architecture analytique pour une librairie
- Equipe, encadrement, date

## Slide 2 - Contexte et objectif

- Système de vente de livres
- Besoin de transformer les données de ventes
- Objectif : construire une OBT exploitable pour l'analyse

## Slide 3 - Cahier des charges

- Snowflake pour l'entrepot
- dbt pour les transformations
- Airflow pour l'orchestration
- Visualisation au choix

## Slide 4 - Architecture globale

- PostgreSQL local
- Ingestion vers Snowflake RAW
- dbt vers STAGGING, WAREHOUSE, MARTS
- Streamlit pour la restitution

## Slide 5 - Modèle de données source

- category
- books
- customers
- factures
- ventes

## Slide 6 - Ingestion

- Création de la base PostgreSQL locale
- Insertion des données d'exemple
- Chargement dans Snowflake RAW via Airflow

## Slide 7 - Transformations STAGGING

- Conversion des dates
- Normalisation des tables
- Création des tables `stg_*`

## Slide 8 - Transformations WAREHOUSE

- Dimensions clients, livres, catégories
- Faits ventes et factures
- Agrégats par année, mois et jour

## Slide 9 - Table MARTS OBT

- Présentation de `MARTS.obt_sales`
- Principaux champs
- Valeur métier pour le reporting

## Slide 10 - Orchestration Airflow

- DAG principal
- Enchainement des tâches
- Automatisation du pipeline

## Slide 11 - Dashboard

- KPI
- Graphiques de ventes
- Analyse clients et livres

## Slide 12 - Conclusion

- Résultats obtenus
- Points forts
- Perspectives d'amélioration
