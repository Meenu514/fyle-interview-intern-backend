# Running with docker

## Build image

- Build the docker image using following command

    ```bash
    docker build -t fyle-backend:latest .
    ```

## Create sqlite database

- If an exsiting DB.sqlite exists, specify it in `docker-compose.yaml` as follows

    ```bash
    volumes:
        - /path/to/file.sqlite3:/home/app/fyle-backend/store.sqlite3:rw
    ```

- OR create an empty DB.sqlite using the following command

    ```bash
    touch store.sqlite3
    ```

## Run container

- Use the docker compose command to run the container as follows

    ```bash
    docker compose up -d
    ```
