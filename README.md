# Project Overview

CFMS is a Complaint and Fault Management System, with Customers and Agents, where Customers can submit and track complaints and Agents & Admins can discuss and move the status of the Complaints throughout the workflow until it is eventually closed.

It also implements a Chatbot, which uses natural language to query the backend data and present it cleanly to the Customers.

# Prerequisites

Docker is required to build and run this application. Please see platform specific instructions below.

## Windows

1. Download and install Docker Desktop.
    1. Ensure that WSL2 is also installed and running as well. 
2. Ensure Docker Desktop is actively running before attempting to build/run the application.

# Environment Setup

To prepare the Environment variables, when you clone the repo, `cd` into the `cfms` folder and run the following:

```bash
cp .env.example .env
```

Then update the `.env` with the changes you'll need. See the section below for descriptions and defaults regarding the `.env` file.

## Environment Variables

| Variable               | Description                                                                                                                                   |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `DJANGO_SECRET_KEY`    | A secret key used by Django for cryptographic signing (sessions, tokens, password resets). Must be kept private in production.                |
| `DEBUG`                | Enables or disables Django debug mode. `True` shows detailed error pages (development only), `False` hides sensitive debug info (production). |
| `DJANGO_LOGLEVEL`      | Sets logging verbosity level (e.g., `debug`, `info`, `warning`, `error`, `critical`). Controls how much log output Django produces.           |
| `DJANGO_ALLOWED_HOSTS` | A list of domain names/IPs that are allowed to serve the Django app. Helps prevent Host header attacks. Example: `localhost`, `example.com`. This is a common seperated list.  |
| `DATABASE_ENGINE`      | Specifies the database backend Django will use. `postgresql_psycopg2` indicates PostgreSQL using the psycopg2 driver.                         |
| `DATABASE_NAME`        | The name of the PostgreSQL database to connect to (e.g., `dockerdjango`).                                                                     |
| `DATABASE_USERNAME`    | Username used to authenticate with the database.                                                                                              |
| `DATABASE_PASSWORD`    | Password for the database user. Should be kept secret and never committed to version control.                                                 |
| `DATABASE_HOST`        | Hostname or service name where the database is running (e.g., `db`).                                                         |
| `DATABASE_PORT`        | Port number for database connection. PostgreSQL default is `5432`.                                                                            |
| `GROQ_API_KEY`         | API key used to authenticate requests to the Groq AI service.                                                                                 |
| `GROQ_MODEL`           | Specifies which Groq-hosted model to use (e.g., `llama-3.1-8b-instant`).                                                                      |


# How to Run

For running for Production & Development, ensure that you clone the application using:

```bash
git clone https://github.com/VishalRamki/dc-assessment.git
```

## Running for Development

Change directory into the `cfms` folder and run the following code.

```bash
python manage.py runserver
```

The code above assumes you have `PostgreSQL` running already.

This allows you to manage and run all the scripts as much or as little as you want, you'll have to manage all of the applications migrations, seed etc. yourself on the cli.

> If you wish to just get up and running, please create the .env file using the `Environment` section and then follow the `Running for Production Section`.

## Running For Production

Change Directory into `cfms` and run the following:

```bash
docker compose up --build
```

You can optionally attach `-d` to detach. This will take between 15-30 seconds for the migrations and the subsequent seeding service to run.

# How to Seed the Database

The application will be seeded with data after the application's migration script is run. Both the seed and migration scripts are run as docker services. The main app will await the successfully completition of both.

# Default Login Credentials

| Role     | Username          | Email                                           | Password   |
| -------- | ----------------- | ----------------------------------------------- | ---------- |
| Customer | `customer_emily`  | [emily@gmail.com](mailto:emily@gmail.com)       | Password.1 |
| Customer | `customer_james`  | [james@gmail.com](mailto:james@gmail.com)       | Password.1 |
| Customer | `customer_sophia` | [sophia@gmail.com](mailto:sophia@gmail.com)     | Password.1 |
| Customer | `customer_daniel` | [daniel@gmail.com](mailto:daniel@gmail.com)     | Password.1 |
| Customer | `customer_olivia` | [olivia@gmail.com](mailto:olivia@gmail.com)     | Password.1 |
| Agent    | `agent_maria`     | [maria@support.com](mailto:maria@support.com)   | Password.1 |
| Agent    | `agent_noah`      | [noah@support.com](mailto:noah@support.com)     | Password.1 |
| Agent    | `agent_ava`       | [ava@support.com](mailto:ava@support.com)       | Password.1 |
| Admin    | `admin_rachel`    | [rachel@company.com](mailto:rachel@company.com) | Password.1 |


# Chatbot Setup

In order for the Chatbot to work correctly, you are required to have a `Groq` Api Key and then specify which `Groq` model you want to use. See the `Environment Variables` section for more information.

# Assumptions & Design Decisions

- I am aware using `nginx` to serve the static files was preferable, however, I wanted to just get this done, and I made the decision to use as simple of a setup as I could to get the application built.

- In my projects, and as part of practices, I am using a seperate `seed-service` that runs after the database has migrated. I will be using the built in `django fixtures` feature to handle this.

- I will not be implementing Customer Sign-Up, Forgot Password, and other account related features. This was not requested in the project description.

- In the chatbot, after several attempts and several versions of tool/mcp use, I narrowed it down to a small library of intents and filters that are extracted from the query using groq then data is filtered out and send back to groq to make it human readable. 