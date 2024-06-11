{{ config(materialized='table') }}

with sales_data as (
    select * from {{ ref('stg_videogame_salesdata') }}
)

select 
    --Identifier
    Game_Id,

    --Game Info
    Name,
    Platform, 
    coalesce(Year_of_Release,0) as Year_of_Release,
    Genre,
    Publisher,

    --Converting Sales Data from Million notation to normal. Convert null to 0 when applicable
    coalesce(NA_Sales*1000000,0) as NA_Sales,
    coalesce(EU_Sales*1000000,0) as EU_Sales,
    coalesce(JP_Sales*1000000,0) as JP_Sales,
    coalesce(Other_Sales*1000000,0) as Other_Sales,
    coalesce(Global_Sales*1000000,0) as Global_Sales,

    --Game Rating
    Critic_Score,
    {{ get_critic_score_category('Critic_Score') }} as Critic_Score_Category,
    User_Score,
    {{ get_user_score_category('User_Score') }} as User_Score_Category,
    ESRB_Rating,
    {{ get_ESRB_rating_full_form('ESRB_Rating') }} as ESRB_Rating_Full_Form
from 
    sales_data