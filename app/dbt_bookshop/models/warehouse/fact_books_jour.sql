select
    b.id as book_id,
    b.code as book_code,
    b.intitule as book_intitule,
    v.annees,
    v.mois,
    v.jour,
    sum(v.qte) as qte_vendue,
    sum(v.qte * v.pu) as montant_vente
from {{ ref('fact_ventes') }} v
join {{ ref('dim_books') }} b on v.book_id = b.id
group by 1, 2, 3, 4, 5, 6
