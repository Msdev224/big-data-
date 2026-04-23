select
    id,
    code,
    first_name,
    last_name,
    trim(first_name || ' ' || last_name) as nom,
    email,
    city,
    country
from {{ ref('stg_customers') }}
