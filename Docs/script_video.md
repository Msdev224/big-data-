# Script de video complet

## Objectif

Cette video doit montrer clairement :

- le sujet du projet
- l'architecture mise en place
- le pipeline complet de la source locale jusqu'a Snowflake
- l'orchestration avec Airflow
- le resultat final avec le dashboard

## Duree conseillee

- entre 4 minutes 30 et 6 minutes

## Avant de commencer l'enregistrement

Faire ces verifications avant de lancer la capture :

- ouvrir le projet dans votre editeur
- avoir Snowflake deja connecte
- avoir Airflow deja lance sur `http://localhost:8080`
- avoir Streamlit deja lance sur `http://localhost:8501`
- avoir le DAG `bookshop_pipeline` deja execute avec succes
- avoir les requetes de verification pretes dans Snowflake

## Ordre des fenetres a preparer

Preparez ces fenetres dans cet ordre pour gagner du temps :

1. editeur de code sur le projet
2. fichier `README.md`
3. fichiers SQL source
4. projet dbt
5. Airflow
6. Snowflake
7. dashboard Streamlit

## Conseils de narration

- parler lentement et clairement
- faire des phrases courtes
- ne pas lire trop vite
- laisser 1 a 2 secondes de pause entre deux ecrans
- toujours annoncer ce que vous montrez

## Script detaille

### Sequence 1 - Introduction

**Duree conseillee**

- 20 a 30 secondes

**Ce que vous affichez**

- le fichier [README.md](/Users/msdev224/Desktop/big%20data/README.md#L1)

**Ce que vous faites**

- ouvrir le projet
- placer le curseur en haut du `README`

**Ce que vous dites**

"Bonjour, dans cette video je vais presenter notre projet d'Architecture Big Data. Le sujet consiste a mettre en place une chaine complete de traitement pour des ventes de livres, avec comme objectif final la construction d'une table OBT exploitable pour l'analyse."

"Dans notre solution, nous avons choisi PostgreSQL comme source locale, Snowflake comme data warehouse, dbt pour les transformations, Airflow pour l'orchestration et Streamlit pour la visualisation."

### Sequence 2 - Vue globale du projet

**Duree conseillee**

- 25 a 35 secondes

**Ce que vous affichez**

- l'arborescence du projet

**Ce que vous faites**

- montrer les dossiers `sql`, `airflow`, `app`, `docs`

**Ce que vous dites**

"Ici, nous avons l'organisation complete du projet. Le dossier sql contient les scripts de creation et d'alimentation des donnees. Le dossier airflow contient le DAG d'orchestration. Le dossier app contient le projet dbt ainsi que le dashboard Streamlit. Enfin, le dossier docs contient les livrables de presentation, de rapport et de demonstration."

### Sequence 3 - Base source PostgreSQL

**Duree conseillee**

- 35 a 45 secondes

**Ce que vous affichez**

- [sql/postgres/01_schema.sql](/Desktop/big%20data/sql/postgres/01_schema.sql#L1)
- puis [sql/postgres/02_seed.sql](/Desktop/big%20data/sql/postgres/02_seed.sql#L1)

**Ce que vous faites**

- montrer les tables
- faire defiler doucement

**Ce que vous dites**

"La premiere etape de notre projet est la creation d'une base locale PostgreSQL, qui joue le role de source transactionnelle. Nous avons cinq tables principales : category, books, customers, factures et ventes."

"Dans le second script, nous inserons des donnees d'exemple. Cela repond a la partie ingestion de la touche personnelle, puisque nous avons une base locale reelle avec des donnees a envoyer vers Snowflake."

### Sequence 4 - Structure cible dans Snowflake

**Duree conseillee**

- 35 a 45 secondes

**Ce que vous affichez**

- [sql/snowflake/01_setup_bookshop.sql](/Users/msdev224/Desktop/big%20data/sql/snowflake/01_setup_bookshop.sql#L1)
- puis Snowflake avec la base `BOOKSHOP`

**Ce que vous faites**

- montrer la creation de la base et des schemas
- ensuite ouvrir Snowflake et afficher les schemas

**Ce que vous dites**

"Dans Snowflake, nous avons cree une base nommee BOOKSHOP, conformement a l'enonce. Cette base contient quatre schemas : RAW, STAGGING, WAREHOUSE et MARTS."

"Le schema RAW recoit les donnees brutes provenant de la base PostgreSQL. Les autres schemas servent respectivement a la preparation, a la modélisation analytique et a la restitution finale."

### Sequence 5 - Tables RAW

**Duree conseillee**

- 20 a 30 secondes

**Ce que vous affichez**

- [sql/snowflake/02_raw_tables.sql](/Users/msdev224/Desktop/big%20data/sql/snowflake/02_raw_tables.sql#L1)
- puis les tables RAW dans Snowflake

**Ce que vous faites**

- montrer que les tables `CATEGORY`, `BOOKS`, `CUSTOMERS`, `FACTURES`, `VENTES` existent

**Ce que vous dites**

"Ici, nous voyons les tables de la zone RAW. Elles conservent la structure source. C'est une etape importante, car elle permet de separer la donnee brute de la donnee transformee."

### Sequence 6 - Projet dbt : couche STAGGING

**Duree conseillee**

- 45 secondes

**Ce que vous affichez**

- [app/dbt_bookshop/models/staging/stg_ventes.sql](/Users/msdev224/Desktop/big%20data/app/dbt_bookshop/models/staging/stg_ventes.sql#L1)
- [app/dbt_bookshop/models/staging/stg_factures.sql](/Users/msdev224/Desktop/big%20data/app/dbt_bookshop/models/staging/stg_factures.sql#L1)

**Ce que vous faites**

- montrer la conversion du champ `date_edit`

**Ce que vous dites**

"Dans la couche STAGGING, nous effectuons les premieres transformations. Le point principal demande dans le sujet est la conversion du champ date_edit, qui arrive au format YYYYMMDD, vers un vrai type DATE."

"Nous faisons cela pour les ventes et pour les factures. Les autres tables, category, books et customers, sont copiees dans des tables stg_ dediees."

### Sequence 7 - Projet dbt : couche WAREHOUSE

**Duree conseillee**

- 1 minute

**Ce que vous affichez**

- [app/dbt_bookshop/models/warehouse/dim_customers.sql](/Users/msdev224/Desktop/big%20data/app/dbt_bookshop/models/warehouse/dim_customers.sql#L1)
- [app/dbt_bookshop/models/warehouse/fact_ventes.sql](/Users/msdev224/Desktop/big%20data/app/dbt_bookshop/models/warehouse/fact_ventes.sql#L1)
- [app/dbt_bookshop/models/warehouse/fact_books_mois.sql](/Users/msdev224/Desktop/big%20data/app/dbt_bookshop/models/warehouse/fact_books_mois.sql#L1)

**Ce que vous faites**

- montrer d'abord les dimensions
- puis les faits
- puis un agregat livres par mois

**Ce que vous dites**

"Dans la couche WAREHOUSE, nous construisons les objets analytiques. Nous creons d'abord les dimensions dim_category, dim_books et dim_customers."

"Pour dim_customers, nous ajoutons la colonne nom, qui est la concatenation de first_name et last_name, comme demande dans l'enonce."

"Ensuite, nous creons les tables de faits fact_ventes et fact_factures. A ce niveau, nous enrichissons les donnees avec les colonnes annees, mois et jour extraites du champ date_edit."

"Enfin, nous creons des agregats complementaires : fact_books_annees, fact_books_mois et fact_books_jour, qui representent les livres vendus selon la temporalite."

### Sequence 8 - Projet dbt : couche MARTS

**Duree conseillee**

- 40 a 50 secondes

**Ce que vous affichez**

- [app/dbt_bookshop/models/marts/obt_sales.sql](/Users/msdev224/Desktop/big%20data/app/dbt_bookshop/models/marts/obt_sales.sql#L1)

**Ce que vous faites**

- montrer la jointure finale

**Ce que vous dites**

"La derniere etape des transformations est la creation de la table MARTS.obt_sales. Cette table correspond a l'OBT demandee dans le sujet."

"Elle regroupe, dans une seule ligne de vente, les informations provenant des ventes, des factures, des livres, des categories et des clients. Cela permet une analyse beaucoup plus simple dans les outils de visualisation."

### Sequence 9 - Tests dbt

**Duree conseillee**

- 20 a 30 secondes

**Ce que vous affichez**

- [app/dbt_bookshop/models/schema.yml](/Users/msdev224/Desktop/big%20data/app/dbt_bookshop/models/schema.yml#L1)

**Ce que vous faites**

- montrer quelques tests `not_null`, `unique`, `relationships`

**Ce que vous dites**

"Nous avons egalement ajoute des tests dbt pour controler la qualite des donnees. Par exemple, nous verifions l'unicite de certains identifiants, la presence obligatoire de certaines colonnes et les relations entre les tables."

### Sequence 10 - Orchestration Airflow

**Duree conseillee**

- 45 a 55 secondes

**Ce que vous affichez**

- [airflow/dags/bookshop_pipeline.py](/Users/msdev224/Desktop/big%20data/airflow/dags/bookshop_pipeline.py#L1)
- puis l'interface Airflow

**Ce que vous faites**

- montrer le DAG
- ensuite ouvrir le graphe du DAG dans Airflow

**Ce que vous dites**

"Pour l'orchestration, nous utilisons Airflow. Le DAG principal s'appelle bookshop_pipeline."

"Il comporte trois grandes etapes. La premiere cree les structures dans Snowflake. La deuxieme ingere les donnees de PostgreSQL vers la zone RAW. La troisieme lance dbt pour executer toutes les transformations jusqu'a MARTS."

"Airflow permet donc d'automatiser et de superviser tout le pipeline."

### Sequence 11 - Verification dans Snowflake

**Duree conseillee**

- 35 a 45 secondes

**Ce que vous affichez**

- [sql/snowflake/03_verification_queries.sql](/Users/msdev224/Desktop/big%20data/sql/snowflake/03_verification_queries.sql#L1)
- puis les resultats dans Snowflake

**Ce que vous faites**

- lancer quelques requetes simples
- montrer que les tables existent
- montrer `MARTS.OBT_SALES`

**Ce que vous dites**

"Apres execution du pipeline, nous verifions que toutes les couches ont bien ete alimentees. Nous controlons la presence des schemas, des tables de staging, des dimensions, des faits et enfin de la table OBT finale."

"Ici, on peut constater que la table MARTS.obt_sales contient bien les donnees attendues."

### Sequence 12 - Dashboard Streamlit

**Duree conseillee**

- 50 a 60 secondes

**Ce que vous affichez**

- le dashboard Streamlit

**Ce que vous faites**

- montrer les KPI
- descendre lentement sur les graphes
- montrer enfin l'aperçu de la table

**Ce que vous dites**

"Pour la visualisation, nous avons choisi Streamlit. Le dashboard consomme les donnees de Snowflake et met en avant les indicateurs principaux."

"Nous retrouvons ici le nombre de ventes, le chiffre d'affaires, le montant paye, puis des graphiques sur les ventes par mois, la repartition des livres vendus et les montants payes par client."

"Enfin, nous affichons un apercu detaille de la table MARTS.obt_sales."

### Sequence 13 - Conclusion

**Duree conseillee**

- 20 a 30 secondes

**Ce que vous affichez**

- soit le dashboard
- soit le README

**Ce que vous faites**

- revenir a une vue globale

**Ce que vous dites**

"Pour conclure, notre projet met en place une architecture Big Data complete allant d'une source locale PostgreSQL jusqu'a une restitution analytique exploitable."

"Nous avons respecte l'esprit du sujet en utilisant Snowflake, dbt et Airflow, puis en ajoutant une visualisation pour valoriser les resultats. Merci."

## Version tres courte a memoriser

Si vous voulez une version plus simple a retenir, voici le fil conducteur :

- presentation du sujet
- presentation de l'architecture
- source PostgreSQL
- chargement Snowflake RAW
- transformations dbt
- orchestration Airflow
- verification Snowflake
- dashboard final
- conclusion

## Conseils de tournage

- ne pas faire de mouvements trop rapides
- zoomer seulement si necessaire
- garder la souris visible
- faire des transitions simples
- si vous hesitez, refaire la phrase plutot que continuer en etant confus

## Plan ideal de capture

1. enregistrer une premiere prise complete
2. noter les passages rates
3. refaire seulement les sequences faibles
4. monter les meilleures parties
