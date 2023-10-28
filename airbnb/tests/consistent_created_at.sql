WITH l AS (
    SELECT * FROM {{ ref('dim_listings_cleansed') }}
),
r AS (
    SELECT * FROM {{ ref("fct_reviews") }}
)


SELECT * FROM l
INNER JOIN r
USING (listing_id)
WHERE l.created_at >= r.review_date