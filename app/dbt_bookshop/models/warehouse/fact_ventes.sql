select
    id,
    facture_id,
    book_id,
    pu,
    qte,
    date_edit,
    extract(year from date_edit) as annees,
    {{ mois_fr('date_edit') }} as mois,
    {{ jour_fr('date_edit') }} as jour
from {{ ref('stg_ventes') }}
