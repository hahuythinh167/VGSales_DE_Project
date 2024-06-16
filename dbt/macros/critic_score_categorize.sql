{# This macro returns the category of the critic rating score #}

{% macro get_critic_score_category(critic_score) -%}

    case 
        when {{ critic_score }} is null then null
        when {{ critic_score }} >= 85 then 'Excellent'
        when {{ critic_score }} >= 70 then 'Okay'
        else 'Bad'
    end

{%- endmacro %}