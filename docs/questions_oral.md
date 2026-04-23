# Questions possibles a l'oral

## Pourquoi avoir choisi Snowflake ?

Snowflake est explicitement recommandé dans l'énoncé, il est adapté aux architectures analytiques
cloud et permet de séparer le stockage du calcul.

## Pourquoi dbt au lieu de Spark ?

dbt est plus simple à mettre en place pour des transformations SQL orientées entrepôt de données.
Il convient bien à un projet pédagogique basé sur Snowflake.

## Quel est le rôle de la couche STAGGING ?

Elle sert à nettoyer et normaliser les données sources sans encore entrer dans la logique métier
analytique.

## Quel est l'intérêt de WAREHOUSE ?

WAREHOUSE contient les dimensions, les faits et les agrégats métier. C'est la couche analytique
intermédiaire avant la restitution.

## Pourquoi créer une OBT dans MARTS ?

Une OBT facilite la consommation par les outils de BI et les dashboards, car toutes les
informations utiles à l'analyse d'une ligne de vente sont centralisées.

## Quel est le rôle d'Airflow ?

Airflow orchestre les différentes étapes du pipeline et permet de rejouer les traitements de façon
structurée et traçable.

## Pourquoi une base PostgreSQL locale ?

Cela répond à la touche personnelle sur l'ingestion en simulant une vraie source transactionnelle.

## Quelles sont les limites actuelles du projet ?

- jeu de données restreint
- absence de gestion d'historisation lente
- absence de tests de qualité avancés
- pas de gestion CI/CD

## Quelles améliorations proposeriez-vous ?

- ajouter davantage de tests dbt
- historiser les dimensions
- créer plus de dashboards
- ajouter des alertes Airflow et de la supervision
