# hillel_fastapi_example

Example project for hillel IT school.

## Set up:
* add .env file based on .env.template in project root, or use other tools to set up environment variables
* create admin user
  * If you are using docker container:
    ```bash
    docker-compose exec web python create_admin.py admin@noreply.com admin
    ```
  * If you run application locally:
    * Make sure you have exported all virtual environment variables
    ```
    python python create_admin.py admin@noreply.com admin
    ```
## Run:

* run all containers using docker-compose
    ```bash
    docker-compose up -d 
    ``` 
* stop all containers using docker-compose
    ```bash
    docker-compose stop
    ```
* remove all containers using docker-compose
    ```bash
    docker-compose down
    ```
