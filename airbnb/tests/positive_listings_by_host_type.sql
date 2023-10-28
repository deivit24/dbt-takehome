SELECT 
    * 
FROM {{ ref("mart_positive_listing_by_host_type") }}
WHERE avg_positive_percentage < .54
AND type_of_listing = 'IS_SUPERHOST'
LIMIT 10
