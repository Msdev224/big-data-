use database BOOKSHOP;

show schemas;

show tables in schema BOOKSHOP.RAW;
show tables in schema BOOKSHOP.STAGGING;
show tables in schema BOOKSHOP.WAREHOUSE;
show tables in schema BOOKSHOP.MARTS;

select count(*) as nb_category from BOOKSHOP.RAW.CATEGORY;
select count(*) as nb_books from BOOKSHOP.RAW.BOOKS;
select count(*) as nb_customers from BOOKSHOP.RAW.CUSTOMERS;
select count(*) as nb_factures from BOOKSHOP.RAW.FACTURES;
select count(*) as nb_ventes from BOOKSHOP.RAW.VENTES;

select count(*) as nb_stg_ventes from BOOKSHOP.STAGGING.STG_VENTES;
select count(*) as nb_stg_factures from BOOKSHOP.STAGGING.STG_FACTURES;
select count(*) as nb_stg_books from BOOKSHOP.STAGGING.STG_BOOKS;
select count(*) as nb_stg_category from BOOKSHOP.STAGGING.STG_CATEGORY;
select count(*) as nb_stg_customers from BOOKSHOP.STAGGING.STG_CUSTOMERS;

select count(*) as nb_dim_category from BOOKSHOP.WAREHOUSE.DIM_CATEGORY;
select count(*) as nb_dim_books from BOOKSHOP.WAREHOUSE.DIM_BOOKS;
select count(*) as nb_dim_customers from BOOKSHOP.WAREHOUSE.DIM_CUSTOMERS;
select count(*) as nb_fact_ventes from BOOKSHOP.WAREHOUSE.FACT_VENTES;
select count(*) as nb_fact_factures from BOOKSHOP.WAREHOUSE.FACT_FACTURES;
select count(*) as nb_fact_books_annees from BOOKSHOP.WAREHOUSE.FACT_BOOKS_ANNEES;
select count(*) as nb_fact_books_mois from BOOKSHOP.WAREHOUSE.FACT_BOOKS_MOIS;
select count(*) as nb_fact_books_jour from BOOKSHOP.WAREHOUSE.FACT_BOOKS_JOUR;

select count(*) as nb_obt_sales from BOOKSHOP.MARTS.OBT_SALES;

select * from BOOKSHOP.MARTS.OBT_SALES order by vente_id;
