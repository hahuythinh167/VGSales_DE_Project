{{ config(materialized='table') }}

with salesdata as {
    select * from {{ ref('stg_videogame_salesdata') }}
}