{{ config(materialized='view') }}

with salesdata as (
    select *,
        row_number() over(partition by Name, Platform) as rn
    from {{ source('staging','VGSales_table')}}
)

select 
    --Identifiers
    {{ dbt_utils.generate_surrogate_key(['Name','Platform','Year_of_Release']) }} as Game_Id,
    

    --Game Info
    Name,
    Platform,
    coalesce(cast(Year_of_Release as integer),0) as Year_of_Release,
    Genre,
    Publisher,

    --Sales Info
    cast(NA_Sales as numeric) as NA_Sales,
    cast(EU_Sales as numeric) as EU_Sales,
    cast(JP_Sales as numeric) as JP_Sales,
    cast(Other_Sales as numeric) as Other_Sales,
    cast(Global_Sales as numeric) as Global_Sales,

    --Ratings 
    cast(Critic_Score as integer) as Critic_Score,
    cast(Critic_Count as integer) as Critic_Count,
    cast(User_Score as integer) as User_Score,
    cast(User_Count as integer) as User_Count,
    Rating
    
from salesdata

where rn = 1

{% if var('is_test_run', default=true) %}
    limit 100
{% endif %}