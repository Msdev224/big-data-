{% macro mois_fr(column_name) -%}
case extract(month from {{ column_name }})
    when 1 then 'janvier'
    when 2 then 'fevrier'
    when 3 then 'mars'
    when 4 then 'avril'
    when 5 then 'mai'
    when 6 then 'juin'
    when 7 then 'juillet'
    when 8 then 'aout'
    when 9 then 'septembre'
    when 10 then 'octobre'
    when 11 then 'novembre'
    when 12 then 'decembre'
end
{%- endmacro %}

{% macro jour_fr(column_name) -%}
case dayofweekiso({{ column_name }})
    when 1 then 'lundi'
    when 2 then 'mardi'
    when 3 then 'mercredi'
    when 4 then 'jeudi'
    when 5 then 'vendredi'
    when 6 then 'samedi'
    when 7 then 'dimanche'
end
{%- endmacro %}
