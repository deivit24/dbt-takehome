{{
  config(
    materialized = 'table'
  )
}}

{# 
    Here is where you got to make changes and add your dbt code. make sure you run dbt_run before
    running dbt test.

    Please updated the code below to make test pass

    Hint use  'dim_listings_with_hosts' and 'fct_reviews' as refs to make this new model

#}

SELECT * FROM {{ ref('dim_listings_with_hosts') }}
