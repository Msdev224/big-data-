select
    id,
    category_id,
    code,
    intitule,
    isbn_10,
    isbn_13,
    prix_catalogue
from {{ source('raw', 'books') }}
