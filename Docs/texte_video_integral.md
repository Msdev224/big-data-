# Texte video integral

## Version complete a dire

Bonjour.

Dans cette video, je vais vous presenter notre projet d'Architecture Big Data. Le sujet consiste a mettre en place une chaine complete de traitement de donnees pour une structure qui vend des livres. L'objectif principal est de transformer des donnees brutes issues du systeme de vente afin de produire une table OBT, c'est-a-dire une table analytique unique, exploitable pour le reporting et la visualisation.

Pour realiser ce projet, nous avons choisi une architecture composee de PostgreSQL comme source locale, Snowflake comme data warehouse, dbt pour les transformations, Airflow pour l'orchestration et Streamlit pour la visualisation finale.

Je vais maintenant presenter le projet de maniere progressive, depuis la source de donnees jusqu'au resultat final.

Ici, nous voyons l'organisation generale du projet. Le dossier sql contient les scripts de creation des tables et les scripts d'alimentation des donnees. Le dossier airflow contient le DAG d'orchestration. Le dossier app contient a la fois le projet dbt et le dashboard Streamlit. Enfin, le dossier docs contient tous les livrables de presentation, de demonstration et de soutenance.

La premiere etape de notre projet est la creation d'une base locale PostgreSQL. Cette base joue le role de source transactionnelle. Nous avons defini cinq tables principales qui representent le fonctionnement metier de la librairie.

La table category contient les categories de livres.

La table books contient les informations sur les livres, comme leur code, leur intitule et leurs ISBN.

La table customers contient les informations sur les clients.

La table factures represente les entetes de facture.

Et enfin, la table ventes represente les lignes de vente.

Dans le script d'alimentation, nous avons ensuite ajoute des donnees d'exemple. Cela nous permet de simuler un vrai contexte metier, avec des clients, des livres, des factures et des ventes. Cette partie repond egalement a la touche personnelle demandee dans le sujet, puisque nous avons mis en place une base locale complete avant l'ingestion dans Snowflake.

Apres la source locale, nous passons a la cible analytique dans Snowflake.

Dans Snowflake, nous avons cree une base de donnees nommee BOOKSHOP, comme demande dans l'enonce. Cette base contient quatre schemas.

Le premier schema est RAW. Il sert a stocker les donnees brutes, c'est-a-dire une copie des donnees source.

Le deuxieme schema est STAGGING. Il sert a preparer et nettoyer les donnees.

Le troisieme schema est WAREHOUSE. Il contient les dimensions, les faits et les agregats metier.

Le quatrieme schema est MARTS. Il contient la table finale orientee consommation.

Dans le schema RAW, nous avons cree les tables CATEGORY, BOOKS, CUSTOMERS, FACTURES et VENTES. Ces tables conservent la structure de la source locale. L'idee ici est de ne pas transformer tout de suite la donnee brute, afin de garder une base propre et traçable.

Une fois les donnees chargees dans RAW, nous utilisons dbt pour effectuer les transformations.

Dans la couche STAGGING, nous realisons les premieres transformations techniques. Le point le plus important impose par le sujet concerne le champ date_edit dans les tables ventes et factures. Dans la source, ce champ est stocke au format YYYYMMDD. Dans STAGGING, nous le convertissons en vrai type DATE.

Nous obtenons ainsi les tables stg_ventes et stg_factures, qui contiennent des dates exploitables pour les analyses temporelles.

En plus de cela, nous copions les tables category, books et customers dans les tables stg_category, stg_books et stg_customers.

Au final, le schema STAGGING contient bien les cinq tables attendues commencant par le prefixe stg_.

Nous passons ensuite a la couche WAREHOUSE, qui correspond a la partie analytique du projet.

Dans cette couche, nous construisons d'abord les dimensions.

La table dim_category est une copie structuree de la table des categories.

La table dim_books reprend les informations des livres.

Et la table dim_customers reprend les clients, avec un enrichissement important demande dans le sujet : l'ajout de la colonne nom, qui correspond a la concatenation de first_name et last_name.

Ensuite, nous construisons les tables de faits.

La table fact_ventes est basee sur stg_ventes. Nous y ajoutons trois colonnes derivees de la date : annees, mois et jour.

La table fact_factures est basee sur stg_factures, avec le meme principe d'enrichissement temporel.

Ces colonnes permettent de faire plus facilement des analyses temporelles sans recalculer a chaque fois les composantes de date.

Toujours dans WAREHOUSE, nous avons aussi cree des tables d'agregation supplementaires.

La table fact_books_annees represente la liste des livres vendus par annee.

La table fact_books_mois represente la liste des livres vendus par mois.

Et la table fact_books_jour represente la liste des livres vendus par jour.

Ces tables permettent de produire des indicateurs synthetiques plus facilement.

Nous arrivons ensuite a la couche MARTS, qui correspond au resultat final du projet.

L'objectif de cette couche est d'obtenir une seule table nommee obt_sales.

Cette table regroupe dans une meme ligne toutes les informations necessaires pour identifier et analyser une vente.

On y retrouve l'identifiant de la vente, l'annee, le mois, le jour, le prix unitaire et la quantite provenant de fact_ventes.

On y retrouve aussi les informations de facture, comme le code de facture, la quantite totale, le montant total et le montant paye.

Ensuite, on ajoute les informations de categorie, les informations de livre comme le code, le titre et les ISBN, ainsi que les informations client, notamment le code client et le nom complet.

Cette table finale simplifie beaucoup la visualisation et le reporting, car toutes les informations utiles sont deja rassemblees dans un meme objet.

En plus des transformations, nous avons egalement ajoute des tests dans dbt afin de controler la qualite des donnees.

Nous verifions par exemple que certains identifiants ne sont pas nuls, qu'ils sont uniques, et que les relations entre les tables sont coherentes.

Cela permet de renforcer la fiabilite du pipeline.

Pour l'orchestration, nous utilisons Airflow.

Le DAG principal s'appelle bookshop_pipeline.

Ce DAG organise le projet en trois grandes etapes.

La premiere etape cree les structures dans Snowflake, c'est-a-dire la base, les schemas et les tables RAW.

La deuxieme etape recupere les donnees depuis PostgreSQL et les charge dans BOOKSHOP.RAW.

La troisieme etape execute dbt afin de construire toutes les couches jusqu'a MARTS.

L'interet d'Airflow est d'automatiser les traitements, de visualiser leur ordre d'execution et de faciliter la supervision du pipeline.

Apres execution du pipeline, nous pouvons verifier directement dans Snowflake que les couches ont bien ete alimentees.

Nous verifions d'abord la presence des schemas RAW, STAGGING, WAREHOUSE et MARTS.

Nous verifions ensuite la presence des tables de staging, des dimensions, des faits et enfin de la table MARTS.obt_sales.

Nous pouvons aussi afficher le contenu de la table obt_sales pour constater que les donnees sont bien consolidees.

La derniere partie du projet concerne la visualisation.

Pour cela, nous avons choisi Streamlit.

Le dashboard se connecte a Snowflake et affiche les informations les plus utiles pour l'analyse.

Nous y trouvons d'abord des indicateurs globaux, comme le nombre de ventes, le chiffre d'affaires total et le montant total paye.

Ensuite, nous avons un graphique des ventes par mois, qui permet de voir l'evolution de l'activite.

Nous avons aussi une visualisation de la repartition des ventes par livre, ce qui permet d'identifier les ouvrages les plus vendus.

Enfin, nous affichons les montants payes par client ainsi qu'un apercu detaille de la table OBT finale.

Cette visualisation repond a la touche personnelle du sujet, qui demandait de mettre en oeuvre une solution de restitution a partir des donnees de WAREHOUSE et de MARTS.

Pour conclure, notre projet met en place une architecture Big Data complete, depuis une source locale PostgreSQL jusqu'a une restitution analytique exploitable.

Nous avons respecte l'esprit du sujet en utilisant Snowflake comme data warehouse, dbt pour les transformations, Airflow pour l'orchestration et Streamlit pour la visualisation.

La solution obtenue est lisible, automatisee, evolutive et adaptee a l'analyse des ventes de livres.

Merci pour votre attention.

## Version plus naturelle a dire

Bonjour.

Dans cette video, je vais vous presenter notre projet d'Architecture Big Data. Le but etait de partir d'un systeme de vente de livres et de construire une chaine complete de traitement pour obtenir une table analytique finale, exploitable pour le reporting.

Pour cela, nous avons choisi PostgreSQL comme source locale, Snowflake comme data warehouse, dbt pour les transformations, Airflow pour l'orchestration et Streamlit pour la visualisation.

Au niveau de l'organisation du projet, le dossier sql contient les scripts de base de donnees, le dossier airflow contient le pipeline d'orchestration, le dossier app contient dbt et le dashboard, et le dossier docs contient les livrables de soutenance.

La premiere etape a ete de mettre en place une base locale PostgreSQL avec cinq tables metier : les categories, les livres, les clients, les factures et les ventes. Nous avons ensuite ajoute des donnees d'exemple pour simuler un vrai contexte de librairie.

Ensuite, dans Snowflake, nous avons cree une base BOOKSHOP avec quatre schemas : RAW, STAGGING, WAREHOUSE et MARTS. Le schema RAW contient la copie brute des donnees source.

Avec dbt, nous transformons ensuite les donnees. Dans STAGGING, nous convertissons notamment les champs date_edit de ventes et factures en vrai format DATE. Puis, dans WAREHOUSE, nous construisons les dimensions et les faits, avec des enrichissements comme l'ajout du nom complet du client et l'extraction de l'annee, du mois et du jour.

Nous construisons aussi des agregats de ventes de livres par annee, par mois et par jour.

Dans MARTS, nous creons enfin la table obt_sales, qui regroupe dans une seule ligne toutes les informations utiles sur une vente : la vente elle-meme, la facture, le livre, la categorie et le client.

Pour automatiser toute cette chaine, nous utilisons Airflow. Le DAG cree les structures dans Snowflake, charge les donnees brutes depuis PostgreSQL et lance ensuite dbt pour construire les couches analytiques.

Une fois le pipeline execute, nous verifions dans Snowflake que toutes les tables sont bien presentes et que la table finale obt_sales contient les donnees attendues.

Enfin, nous utilisons Streamlit pour visualiser les resultats. Le dashboard affiche les KPI principaux, les ventes par mois, la repartition des livres vendus, les paiements par client et un apercu de la table finale.

Pour conclure, ce projet nous a permis de mettre en oeuvre une architecture Big Data complete, automatisee et orientee analyse, en respectant les attentes principales du sujet.

Merci.

## Version courte si vous stressez

Bonjour.

Dans cette video, je presente notre projet d'Architecture Big Data sur les ventes de livres.

Nous avons utilise PostgreSQL comme source locale, Snowflake comme data warehouse, dbt pour les transformations, Airflow pour l'orchestration et Streamlit pour la visualisation.

Nous avons d'abord cree les tables source et insere des donnees d'exemple dans PostgreSQL.

Ensuite, nous avons charge ces donnees dans Snowflake, dans le schema RAW.

Avec dbt, nous avons construit les couches STAGGING, WAREHOUSE et MARTS.

Dans WAREHOUSE, nous avons cree les dimensions, les faits et les agregats.

Dans MARTS, nous avons cree la table finale obt_sales, qui regroupe toutes les informations utiles sur les ventes.

Airflow nous permet d'automatiser toute cette chaine.

Enfin, Streamlit nous permet de visualiser les resultats avec des indicateurs et des graphiques.

Ce projet montre donc une architecture complete, depuis la source locale jusqu'a la restitution finale.

Merci.
