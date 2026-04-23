# Contenu détaillé des slides

## Slide 1 - Titre

- Projet Big Data M2
- Mise en place d'une architecture analytique pour une librairie
- Equipe de 3 personnes

## Slide 2 - Problématique

- La structure dispose d'un système de vente des livres
- Les données sont opérationnelles, mais peu exploitables pour l'analyse
- Il faut produire une OBT permettant de suivre les ventes, les clients et les livres

## Slide 3 - Objectifs

- Centraliser les données dans Snowflake
- Structurer les données en couches `RAW`, `STAGGING`, `WAREHOUSE`, `MARTS`
- Orchestrer la chaîne avec Airflow
- Rendre les résultats visibles avec un dashboard

## Slide 4 - Architecture choisie

- PostgreSQL local comme source
- Airflow pour l'ingestion et l'orchestration
- Snowflake comme data warehouse cloud
- dbt pour les transformations
- Streamlit pour la visualisation

## Slide 5 - Données sources

- `category` : catégories de livres
- `books` : catalogue des livres
- `customers` : clients
- `factures` : entêtes de factures
- `ventes` : lignes de ventes

## Slide 6 - Couche RAW

- Reçoit les données brutes depuis PostgreSQL
- Conserve la structure source
- Sert de point d'entrée fiable pour le pipeline

## Slide 7 - Couche STAGGING

- Conversion des champs `date_edit` au format `DATE`
- Copie standardisée des tables métiers
- Préparation des données avant modélisation analytique

## Slide 8 - Couche WAREHOUSE

- Dimensions `dim_customers`, `dim_books`, `dim_category`
- Faits `fact_ventes`, `fact_factures`
- Agrégats de ventes par année, mois et jour

## Slide 9 - Couche MARTS

- Une seule table `obt_sales`
- Vue consolidée de chaque ligne de vente
- Jointure entre ventes, factures, clients, livres et catégories

## Slide 10 - Airflow

- Création des structures Snowflake
- Chargement des données RAW
- Déclenchement du `dbt build`
- Exécution reproductible et automatisable

## Slide 11 - Dashboard

- KPI globaux
- Chiffre d'affaires par mois
- Répartition des ventes par livre
- Paiements par client

## Slide 12 - Valeur ajoutée

- Industrialisation du traitement
- Meilleure lisibilité métier
- Base prête pour du reporting plus avancé

## Slide 13 - Difficultés et solutions

- Diagramme du PDF partiellement non extractible
- Proposition d'un modèle minimal cohérent
- Documentation des hypothèses pour rester transparent

## Slide 14 - Conclusion

- L'objectif du projet est atteint
- La chaîne Big Data complète est présente
- Le projet peut être enrichi par plus de données et plus d'indicateurs
