WITH ReviewSentiment AS (
    SELECT
        {{ ref('fct_reviews') }}.listing_id,
        SUM(CASE WHEN {{ ref('fct_reviews') }}.review_sentiment = 'positive' THEN 1 ELSE 0 END) as positive_count,
        COUNT(*) as total_count
    FROM {{ ref('fct_reviews') }}
    GROUP BY {{ ref('fct_reviews') }}.listing_id
)
SELECT 
    * 
FROM {{ ref("mart_positive_listings") }} AS MPL
LEFT JOIN ReviewSentiment rs ON MPL.listing_id = rs.listing_id
WHERE MPL.positive_percentage != COALESCE(CAST(CAST(rs.positive_count AS FLOAT) / NULLIF(rs.total_count, 0) AS DECIMAL(10, 2)), 0.00)
