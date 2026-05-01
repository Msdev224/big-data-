# Dictionnaire de donnees

## Source PostgreSQL

### `category`

- `id` : identifiant de categorie
- `code` : code categorie
- `intitule` : libelle categorie

### `books`

- `id` : identifiant du livre
- `category_id` : categorie du livre
- `code` : code livre
- `intitule` : titre du livre
- `isbn_10` : ISBN 10
- `isbn_13` : ISBN 13
- `prix_catalogue` : prix catalogue

### `customers`

- `id` : identifiant client
- `code` : code client
- `first_name` : prenom
- `last_name` : nom
- `email` : email
- `city` : ville
- `country` : pays

### `factures`

- `id` : identifiant facture
- `customer_id` : identifiant client
- `code` : code facture
- `qte_totale` : quantite totale de la facture
- `total_amount` : montant total facture
- `total_paid` : montant regle
- `date_edit` : date au format `YYYYMMDD`

### `ventes`

- `id` : identifiant de ligne de vente
- `facture_id` : identifiant facture
- `book_id` : identifiant livre
- `pu` : prix unitaire
- `qte` : quantite
- `date_edit` : date au format `YYYYMMDD`

## STAGGING

### `stg_ventes`

- copie de `RAW.ventes`
- conversion de `date_edit` en type `DATE`

### `stg_factures`

- copie de `RAW.factures`
- conversion de `date_edit` en type `DATE`

### `stg_books`, `stg_category`, `stg_customers`

- copies standardisees des tables source

## WAREHOUSE

### `dim_customers`

- copie de `stg_customers`
- ajout de `nom = first_name || ' ' || last_name`

### `dim_books`

- copie de `stg_books`

### `dim_category`

- copie de `stg_category`

### `fact_ventes`

- copie de `stg_ventes`
- ajout de `annees`, `mois`, `jour`

### `fact_factures`

- copie de `stg_factures`
- ajout de `annees`, `mois`, `jour`

### `fact_books_annees`

- agregat des ventes par livre et annee

### `fact_books_mois`

- agregat des ventes par livre, annee et mois

### `fact_books_jour`

- agregat des ventes par livre, annee, mois et jour

## MARTS

### `obt_sales`

- table analytique finale
- une ligne par vente
- enrichie avec :
  - infos facture
  - infos livre
  - infos categorie
  - infos client
