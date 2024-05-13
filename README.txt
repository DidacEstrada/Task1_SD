1. Tener ejecutandose Redis en el puerto 6379 i Rabbit en el puerto 5672 i el 15672(para el managment)
    comandas: docker run --name some-redis -p 6379:6379 -d redis
              docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

2. Ejecutar primero el script 'start-server.py'

3. Ejecuctar el script 'start-client.sh'