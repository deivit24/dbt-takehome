Welcome to your dbt test!

### Overview

Congrats on making it this far in the interview process. Take your time in looking around the psotgres tables and dbt code to get yourself familiar


This dbt project had free open source airbnb data:

 - Listings
 - Hosts
 - Reviews

 We seeded raw tables based off these csv files called `raw_hosts`, `raw_listings`, and `raw_reviews`

 In the `airbnb/models/src` directory you see our first set of models:
  - src_hosts.sql
  - src_listings.sql
  - src_reviews.sql

These are the first sets of of models that were created from the src files hence the src prefix. In general
SRC models are your source data, containing raw or lightly transformed data.
  
In the `airbnb/models/dim`, you see another set of models called dimension models.
  - dim_hosts_cleansed.sql
  - dim_listings_cleansed.sql
  - dim_listings_with_hosts.sql
 
 DIM models are used for descriptive information and contain attributes to enrich your data.

In the `airbnb/models/fct`, you see another set of models called fact models.
  - fct_reviews.sql

FCT models store quantitative data and are used for analysis and reporting
 
Lastly you have your Data Marts in `airbnb/models/mart`
 - mart_fullmoon_reviews.sql
 - mart_positive_listing_by_host_type.sql
 - mart_positive_listings.sql

 "MART" (Data Mart) models are specialized subsets of data within your data warehouse. They are designed to serve the specific analytical or reporting needs of different business units or departments within an organization. Data marts typically combine source, dimension, and fact models to create a focused and tailored environment for users to access data relevant to their specific area of interest


 ### Helpful commands

 running `dbt compile` compiles your dbt code to sql and it is stored in `airbnb/target/compiled/airbnb/models` you can paste this query to postgres to see how the code is compiled.

 Also run `dbt docs serve`

 There should be a button on the bottom right (View Lineage Graph). Click on the button and you can see a graph of upstream and downstream models.

 I would filter by resources and and just select `models` and `sources` to see the graph.

 ### Takehome Exam

 We are going to be focusing first on `models/mart/mart_positive_listings.sql`

 The goal here is to created a new model that looks like this:

 | listing_id | listing_name           | price | host_id | host_name     | host_is_superhost (varcahr)| updated_at | positive_percentage |
|------------|------------------------|-------|---------|---------------|-----------------------------|------------|----------------------|
| 101       | Cozy Apartment         | 100   | 1001    | Alice Johnson | t                            | 2023-10-25 | 0.85               |
| 102       | Spacious Loft          | 150   | 1002    | Bob Smith     | f                            | 2023-10-26 | 0.72               |
| 103       | Modern Condo           | 120   | 1003    | Carol White   | t                            | 2023-10-27 | 0.91               |
| 104       | Charming Cottage       | 80    | 1004    | David Brown   | f                            | 2023-10-28 | 0.65               |
| 105       | Luxury Villa           | 300   | 1005    | Emily Davis   | t                            | 2023-10-29 | 0.94               |

Rows are just examples

You can see that this is a join of 'dim_listings_with_hosts' and 'fct_reviews'. 

fct_reviews give you data of all the reviews of listings. So there can be multiple rows with the same listing_id. There is a column called review_sentiment which is either `positve`, `negative` or `neutral`.

The goal is creat a new table that has a percentage of positive reviews. Meaning if listing id has 10 reviews, 7 are positive, 2 are neutral and 1 is negative, the column should have a value of 0.70.

The new model should have distict listing_ids.

Once you created the model, please run `dbt run` to successfully populate your db then run `dbt test`. There should only be two failing afterwards

Once you are successful, you can move on to the next model `models/mart/mart_positive_listing_by_host_type.sql`

The goal here is to create a new model from `mart_positive_listings.sql` that looks like this:

 | type_of_listing | avg_percentage         | 
|------------------|------------------------|
| IS_SUPERHOST     |         0.60           | 
| IS_NOT_SUPERHOST |         0.45           | 

There should only be two rows and the type_of_listing values HAVE to be `IS_SUPERHOST` and `IS_NOT_SUPERHOST`. The avg_percentage in the 
rows above are just examples.

Goal here is to find out the average postive percentage of hosts that are super hosts and average postive percentage of hosts that are not super hosts.

Once you created the model, please run `dbt run` to successfully populate your db then run `dbt test`. There should only be one failing afterwards

The rest is a bonus. 

There is a model in the `airbnb/models/dim` that needs a slight tweak in order to make it work. The failure comes from an upstream model of `mart_positive_listings`.


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
