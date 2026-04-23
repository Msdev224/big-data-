select
    id,
    code,
    first_name,
    last_name,
    email,
    city,
    country
from {{ source('raw', 'customers') }}
