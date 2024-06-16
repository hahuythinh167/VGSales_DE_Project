{# This macro returns the full form of ESRB rating abbreviation #}
{% macro get_ESRB_rating_full_form(ESRB_Rating) -%}

    case 
        when {{ ESRB_Rating }} is null then null
        when {{ ESRB_Rating }} = 'E' then 'Everyone'
        when {{ ESRB_Rating }} = 'E10+' then 'Everyone 10 and older'
        when {{ ESRB_Rating }} = 'T' then 'Teen'
        when {{ ESRB_Rating }} = 'M' then 'Mature 17+'
        when {{ ESRB_Rating }} = 'AO' then 'Adults Only 18+'
        when {{ ESRB_Rating }} = 'RP' then 'Rating Pending'
        when {{ ESRB_Rating }} = 'K-A' then 'Kids to Adults'
        when {{ ESRB_Rating }} = 'EC' then 'Early Childhood'
        else 'Not Sure'
    end

{%- endmacro %}