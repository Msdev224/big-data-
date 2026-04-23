select
    id,
    customer_id,
    code,
    qte_totale,
    total_amount,
    total_paid,
    to_date(date_edit, 'YYYYMMDD') as date_edit
from {{ source('raw', 'factures') }}
