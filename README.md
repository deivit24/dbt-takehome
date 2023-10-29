# Take home DBT project

This is a repo that anyone can clone to get a simple DBT project setup with postgres data setup using docker.

Most DBT projects use data platforms like Snowflake, Databricks and BigQuery. Reason why I choose not to use any of those platforms right now is because it cost money after your free trial is over! If you have ok sql knowledge. This should be enough to get this project setup.

## Recommended VSCODE Extensions:

1. PostgreSQL [Link](https://marketplace.visualstudio.com/items?itemName=ckolkman.vscode-postgres)
2. dbt Power User [Link](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user)
3. Better Jinja [Link](https://marketplace.visualstudio.com/items?itemName=samuelcolvin.jinjahtml)

This will really help with this project but it is not required

## Env Setup

Create an `.env` file at the root of the project and add these environment variables:

```txt
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=WhatEverYouWant
POSTGRES_PASSWORD=WhatEverYouWant
POSTGRES_DB=airbnb
POSTGRES_DRIVER=postgresql
```

Then run `source .env` to make sure you apply the changes. Theses are variables that the `docker-compose.yml` file will pick up

Unforunately, dbt does not support environement variables from `.env` files.

### Linux and maxOS(Zsh)

1. open terminal
2. Use a text editor like nano, vim, or gedit to edit your .zshrc file. For example: `nano ~/.zshrc`
3. Add this: 
    ```txt 
    export POSTGRES_USER="WhatEverYouWant"
    export POSTGRES_PASSWORD="WhatEverYouWant"
    ```
4. Save file and apply changes `source ~/.zshrc`

### Windows
1. Right-click on "This PC" (or "My Computer" in older versions) and select "Properties."
2. In the System window, click "Advanced system settings" on the left side.
3. In the System Properties window, go to the "Advanced" tab and click the "Environment Variables" button.
4. In the "User variables" section, click "New."
5. Enter the name and value for your environment variable.
6. Click "OK" to save the variable.

### Python env Setup

Run

```shell
python -m venv venv
```
Activate Env

```shell
source venv/bin/activate
```

From root run

```shell   
pip install -r requirements.txt
```

### Test DBT Connection

First make sure you have docker running, open up a terminal and from the root run:

```shell
docker-compose up -d
```

This should pull a postgres image and build a container.

Now it is time to load raw source tables and test your DBT connection.

unzip `files.zip` and put csv files in the `airbnb` directory

From root run:

```shell
python seed.py
```

This script connects to your postgres inside of docker and creates raw tables and seeds them.
You can take a look and see three tables that were seeded from the csv files.

then run:

```shell            
cd airbnb
```

Then run:

```shell
dbt debug
```
You should get a message saying stating that all checks have passed! DBT is now successfully connected to postgres that is running on docker

Now we run

```shell
dbt run
```

You should receive a bunch of views and tables being created.

`dbt run` complies and executes sql queries. 

You can now take a look at your postgres and see new tables and views were created from the raw source tables

Now run:

```shell
dbt test
```

This should run the dbt tests and you should see three test failures. If you got three failures you are ready to move on. Please look at the readme.md inside the airbnb directory.

Please do not hesitate to reach out if you run into any issues.

