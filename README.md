# celery_docker
docker-compose up --build

sudo docker container ls

sudo docker container stop xxxx

sudo docker run --rm -d --name celery_scheduler -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro celery_scheduler:latest

sudo docker container exec -it celery_scheduler date
