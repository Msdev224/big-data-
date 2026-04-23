select
    id,
    code,
    intitule
from {{ ref('stg_category') }}
