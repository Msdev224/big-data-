select
    id,
    facture_id,
    book_id,
    pu,
    qte,
    to_date(date_edit, 'YYYYMMDD') as date_edit
from {{ source('raw', 'ventes') }}
