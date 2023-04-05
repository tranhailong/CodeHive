source .env

black .
docker build -t $IMAGE .
#docker run -d -p 9000:9000 --name test $IMAGE
