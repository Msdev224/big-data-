select
    v.id as vente_id,
    v.annees,
    v.mois,
    v.jour,
    v.pu,
    v.qte,
    f.id as facture_id,
    f.code as facture_code,
    f.qte_totale,
    f.total_amount,
    f.total_paid,
    c.intitule as category_intitule,
    b.code as book_code,
    b.intitule as book_intitule,
    b.isbn_10,
    b.isbn_13,
    cu.code as customer_code,
    cu.nom as customer_nom
from {{ ref('fact_ventes') }} v
join {{ ref('fact_factures') }} f on v.facture_id = f.id
join {{ ref('dim_books') }} b on v.book_id = b.id
join {{ ref('dim_category') }} c on b.category_id = c.id
join {{ ref('dim_customers') }} cu on f.customer_id = cu.id
