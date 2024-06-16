{# This macro returns the category of the user rating score #}

{% macro get_user_score_category(user_score) -%}

    case 
        when {{ user_score }} is null then null
        when {{ user_score }} >= 8.5 then 'Excellent'
        when {{ user_score }} >= 7.0 then 'Okay'
        else 'Bad'
    end

{%- endmacro %}