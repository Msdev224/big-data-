# Hypothèses de modélisation

Le document PDF impose les tables métiers et les résultats attendus, mais le détail textuel du
schéma de la page 2 n'est pas entièrement exploitable en extraction simple.

Pour pouvoir livrer un projet complet et cohérent, les hypothèses suivantes ont été retenues :

## Tables source

### `category`

- `id` : identifiant technique
- `code` : code métier de catégorie
- `intitule` : libellé de catégorie

### `books`

- `id` : identifiant technique du livre
- `category_id` : référence vers `category.id`
- `code` : code métier du livre
- `intitule` : titre du livre
- `isbn_10` : ISBN 10
- `isbn_13` : ISBN 13
- `prix_catalogue` : prix catalogue

### `customers`

- `id` : identifiant technique client
- `code` : code client
- `first_name` : prénom
- `last_name` : nom
- `email` : email
- `city` : ville
- `country` : pays

### `factures`

- `id` : identifiant technique facture
- `customer_id` : référence vers `customers.id`
- `code` : code facture
- `qte_totale` : quantité totale
- `total_amount` : montant total
- `total_paid` : montant payé
- `date_edit` : date au format `YYYYMMDD`

### `ventes`

- `id` : identifiant de ligne de vente
- `facture_id` : référence vers `factures.id`
- `book_id` : référence vers `books.id`
- `pu` : prix unitaire vendu
- `qte` : quantité
- `date_edit` : date au format `YYYYMMDD`

## Justification

Ce modèle permet de satisfaire tous les objets demandés dans l'énoncé :

- STAGGING des cinq tables source
- dimensions `customers`, `category`, `books`
- faits `ventes`, `factures`, `books_annees`, `books_mois`, `books_jour`
- OBT finale `marts.obt_sales`

Si vous récupérez le schéma exact du diagramme image, il suffira d'ajuster les colonnes
et les jointures dans :

- `sql/postgres/01_schema.sql`
- `sql/snowflake/02_raw_tables.sql`
- `app/dbt_bookshop/models/`
