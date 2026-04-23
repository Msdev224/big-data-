select
    id,
    code,
    intitule
from {{ source('raw', 'category') }}
