DROP TABLE IF EXISTS ventes;
DROP TABLE IF EXISTS factures;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS category;

CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    intitule VARCHAR(100) NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES category(id),
    code VARCHAR(20) NOT NULL UNIQUE,
    intitule VARCHAR(255) NOT NULL,
    isbn_10 VARCHAR(10) NOT NULL,
    isbn_13 VARCHAR(13) NOT NULL,
    prix_catalogue NUMERIC(10,2) NOT NULL
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE factures (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    code VARCHAR(20) NOT NULL UNIQUE,
    qte_totale INTEGER NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL,
    total_paid NUMERIC(10,2) NOT NULL,
    date_edit VARCHAR(8) NOT NULL
);

CREATE TABLE ventes (
    id INTEGER PRIMARY KEY,
    facture_id INTEGER NOT NULL REFERENCES factures(id),
    book_id INTEGER NOT NULL REFERENCES books(id),
    pu NUMERIC(10,2) NOT NULL,
    qte INTEGER NOT NULL,
    date_edit VARCHAR(8) NOT NULL
);
