###  Getting started:
  #### Running manually

  Server Environment Variables
  Because app depends on database and storage it is important to provide environment variable
  securely in .env
  - Add .env file with given credentials (see .env-sample file for required environments)

  Python Environment
  There are currently two ways how to manage python virtual enironment
  1. using pip and venv
  2. using poetry - it is environment and package manager for the python

  PIP
  - 
  - Install dependencies: `pip install -r requirements.txt`

  Poetry (Recommended)
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

###  Setup environments:
  * create `.env` folder
  * see `.env-sample` for exact env variables 
  * if DB is not created make sure to create instance locally
  * example to create docker container
    * `docker run --name phys-tech-db -e POSTGRES_PASSWORD=mysecretpassword -d postgres`

### PhysTech Admin panel - Access:
  * [Click here for Admin Panel](http://78.40.216.114:8000/admin)
  * or copy this `http://78.40.216.114:8000/admin`
 
### PhysTech Admin - Navigation:
  * Users
    * View all current users
    * Export selected/all users
    * Add/Delete user
    * Search by email, first and last name

  * Organizations
    * View all current organizations
    * Export selected/all organizations
    * Add/Delete organizations
    * Search by email, first and last name

  * Services
    * View all current services
    * Export selected/all services
    * Add/Delete services
    * Search by email, first and last name

  * Service Requests
    * View all current service requests
    * Export selected/all service requests
    * Add/Delete service requests
    * Search by email, first and last name