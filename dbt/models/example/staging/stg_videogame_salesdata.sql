{{ config(materialized='view') }}

with salesdata as (
    select *,
        row_number() over(partition by Name, Platform, Year_of_Release) as rn
    from {{ source('staging','VGSales_table')}}
)

select 
    --Identifiers
    {{ dbt_utils.generate_surrogate_key(['Name','Platform','Year_of_Release']) }} as Game_Id,
    

    --Game Info
    Name,
    Platform,
    safe_cast(Year_of_Release as integer) as Year_of_Release,
    Genre,
    Publisher,

    --Sales Info
    safe_cast(NA_Sales as numeric) as NA_Sales,
    safe_cast(EU_Sales as numeric) as EU_Sales,
    safe_cast(JP_Sales as numeric) as JP_Sales,
    safe_cast(Other_Sales as numeric) as Other_Sales,
    safe_cast(Global_Sales as numeric) as Global_Sales,

    --Ratings 
    safe_cast(Critic_Score as numeric) as Critic_Score,
    safe_cast(Critic_Count as numeric) as Critic_Count,
    safe_cast(User_Score as numeric) as User_Score,
    safe_cast(User_Count as numeric) as User_Count,
    Rating as ESRB_Rating
    
from salesdata

where rn = 1

{% if var('is_test_run', default=true) %}
    limit 100
{% endif %}