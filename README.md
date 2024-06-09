###  Getting started:
  #### Running manually

  Poetry
  - if new to poetry please follow documentation - https://python-poetry.org/docs/
  - Activate venv: `poetry shell`
  - Install dependencies: `poetry install`
  
  Running the Server
  - Run server: `uvicorn main:app --reload`


  #### Running using Docker
  Database is strongly recommended to be run via docker.
  - Add .env file with given credentials
  - `docker-compose -f docker-compose.dev.yml up --build`


---
 
### Migration generate:
  - `alembic revision --rev-id=<revisionId> --autogenerate -m 'your_message'`
  - Example: `alembic revision --rev-id=0001 --autogenerate -m 'your_message'`

###  Migration apply:
  - Specific version
    - `alembic upgrade <revisionId>`
    - `alembic downgrade <revisionId>` 
    - Example `alembic upgrade 6d4bb18b725c`
  - Latest version
    - `alembic upgrade head`

###  Unapply all migrations:
  - `alembic downgrade base`

###  To show all applied migrations:
  * `alembic history`