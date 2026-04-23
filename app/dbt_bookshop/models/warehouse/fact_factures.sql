select
    id,
    customer_id,
    code,
    qte_totale,
    total_amount,
    total_paid,
    date_edit,
    extract(year from date_edit) as annees,
    {{ mois_fr('date_edit') }} as mois,
    {{ jour_fr('date_edit') }} as jour
from {{ ref('stg_factures') }}
