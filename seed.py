from psycopg2 import connect
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()
csv_path = 'airbnb/'

# Get the full path to the CSV files
full_listings_path = os.path.abspath(os.path.join(csv_path, 'listings.csv'))
full_reviews_path = os.path.abspath(os.path.join(csv_path, 'reviews.csv'))
full_hosts_path = os.path.abspath(os.path.join(csv_path, 'hosts.csv'))

CSV_LIST = [full_listings_path, full_reviews_path, full_hosts_path]
DOCKER_CONTAINER_NAME = "airbnb-db"  # Replace with your actual Docker container name

def copy_to_docker(from_path, container_name, to_path):
    try:
        subprocess.run(["docker", "cp", from_path, f"{container_name}:{to_path}"], check=True, text=True)
        print(f"File copied from {from_path} to {container_name}:{to_path} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running the 'docker cp' command: {e}")
    except FileNotFoundError:
        print("Docker command not found. Make sure Docker is installed and available in your PATH.")

for path in CSV_LIST:
    copy_to_docker(path, DOCKER_CONTAINER_NAME, '/usr/local')

db_params = {
    'host': os.environ.get('POSTGRES_HOST'),
    'database': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
}

sql_script = """

DROP SCHEMA IF EXISTS airbnb CASCADE;
CREATE SCHEMA IF NOT EXISTS raw;


DROP TABLE IF EXISTS raw.raw_listings CASCADE;
CREATE TABLE raw.raw_listings (
    id serial PRIMARY KEY,
    listing_url text,
    name text,
    room_type text,
    minimum_nights integer,
    host_id integer,
    price text,
    created_at timestamp,
    updated_at timestamp
);

COPY raw.raw_listings (
    id,
    listing_url,
    name,
    room_type,
    minimum_nights,
    host_id,
    price,
    created_at,
    updated_at
)
FROM '/usr/local/listings.csv' CSV HEADER DELIMITER ',' QUOTE '"';

DROP TABLE IF EXISTS raw.raw_reviews CASCADE;
-- Create the raw_reviews table
CREATE TABLE raw.raw_reviews (
    listing_id integer,
    date timestamp,
    reviewer_name text,
    comments text,
    sentiment text
);

-- Copy data from CSV into the raw_reviews table
COPY raw.raw_reviews (listing_id, date, reviewer_name, comments, sentiment)
FROM '/usr/local/reviews.csv'
CSV HEADER DELIMITER ',' QUOTE '"';

DROP TABLE IF EXISTS raw.raw_hosts CASCADE;
-- Create the raw.raw_hosts table
CREATE TABLE raw.raw_hosts (
    id integer,
    name text,
    is_superhost text,
    created_at timestamp,
    updated_at timestamp
);

-- Copy data from CSV into the raw_hosts table
COPY raw.raw_hosts (id, name, is_superhost, created_at, updated_at)
FROM '/usr/local/hosts.csv'
CSV HEADER DELIMITER ',' QUOTE '"';
"""

try:
    # Connect to the PostgreSQL database
    connection = connect(**db_params)

    # Create a cursor object
    cursor = connection.cursor()

    # Execute the SQL script, passing the full paths as parameters
    cursor.execute(sql_script)

    # Commit the changes
    connection.commit()

    print("SQL script executed successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()