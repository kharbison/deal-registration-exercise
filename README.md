# deal-registration-exercise

For a detailed description and overview of the application please see the [Design Doc](https://github.com/kharbison/deal-registration-exercise/blob/master/docs/design_doc.md).

## Pre-requisites
- [Python v3.6+](https://www.python.org/downloads/)
- [Node.js v12](https://nodejs.org/en/)
- [Docker](https://www.docker.com)
- [PostgreSQL v12 (_optional_)](https://www.postgresql.org)
    * Only necessary if not running containerized PostgreSQL image

## Installation
1. Clone, fork, or download the repository to get the application code.

    ```
    git clone git@github.com:kharbison/deal-registration-exercise.git
    cd deal-registration-exercise
    ```

2. Run script to install local dependencies

    ```
    ./scripts/local_setup.sh
    ```

    * This script will install all dependencies locally for the backend, frontend, and `db-loader`.
    * The biggest thing this script does is package the `db-loader` module so that it can be run as a cmd.
        * See the Populate Database section for details on running this module.

## Deployment
Deploying the application will start docker containers of the frontend, backend, and PostgreSQL database. Before being able to parse any CSV files and add the tables to the database, these containers will need to be started so that the PostgreSQL server is active. Building and starting the containers has all been handled in a single script that can easily be run.

```
./scripts/deploy.sh
```
### Deploying Remotely

If you will be accessing the frontend web page from a location different from where your containers are running, you will need to set a `VUE_APP_API_URL` environment variable to the URL of the backend container. This variable is set to `http://localhost:3000` by default so if you are running everything locally, you will not need to set this. Your URL should be connecting to port 3000 and should not have a trailing `/`.

To set this variable and deploy the containers you would run the following:

```
export VUE_APP_API_URL=http://localhost:3000
./scripts/deploy.sh
```

## Populate Database
The PostgreSQL URL is accepted dynamically so that the `db-loader` can be run with other PostgreSQL database servers if necessary. To run the `db-loader` with the containers started use the cmds below.

1. Set/Create an environment variable named `DEAL_REG_DB_URL` to the PostgreSQL URL. For example the below cmd will set this variable to the URL of the Postgres server if you are running the container locally.

    ```
    export DEAL_REG_DB_URL=postgresql://postgres@localhost:5432/DealRegDB
    ```
    If you decide to run the containers at another location, you will be responsible for setting the correct username, password, and host name of the URL. `DealRegDB` is the name of the database create/access so your URL should always have this value at the end.

    Note: For simplicity, it is recommended that you run the containers locally if possible.

2. Once the PostgreSQL URL is set, run the `db-loader` cmd with the CSV file(s) as arguments.

    ```
    db-loader *.csv
    ```

To update the database at any point, simply run this cmd again with the new CSV files(s). Make sure to set `DEAL_REG_DB_URL` again if you are in a new terminal session.

Note: The PostgreSQL container connects to a volume so all data should persist through stopping and starting the containers.

## Usage

To get the corresponding Deal Registration Group of a specified part number, navigate to the URL at which the containers are being served. You should be connecting to port 8080.

For example, if the containers are running locally, the web page would be located at http://localhost:8080.

Once the page is loaded, simply input a part number and select search to get the corresponding Deal Registration Group of a part number in the database.

## Testing

Tests are set up for the `db-loader` and backend code.
Currently the database connection URL in these tests is hardcoded to `postgresql://postgres@localhost:5432/TestDB` (the URL if the postgres container is running locally). If you would like the tests to connect to a different server you will have to change this manually in the tests.

 To run these tests, you will need to have the containers deployed locally and run the test script.

```
./scripts/test.sh
```

Note: `local_setup.sh` is required to be executed before the `test.sh` script can run.

## Stopping Deployed Containers

Once you have finished executing the app, all containers can be stopped by running the `stop.sh` script.

```
./scripts/stop.sh
```