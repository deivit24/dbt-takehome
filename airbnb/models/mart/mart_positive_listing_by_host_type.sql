{{
  config(
    materialized = 'table'
  )
}}

{# 
    Here is where you got to make changes and add your dbt code. make sure you run dbt_run before
    running dbt test

    Here all it is making a new model out of 'mart_positive_lisitings' as a ref

    Please updated the code below to make test pass
#}

SELECT * FROM {{ ref('mart_positive_listings') }}