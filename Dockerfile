FROM redis:latest

#Establecer directorio de trabajo
WORKDIR /usr/local/etc/redis/

#Copiar configuración de Redis personalizada
COPY redis.conf /usr/local/etc/redis/redis.conf

#Exponer puerto de Redis (por defecto es el 6379)
EXPOSE 6379

#Ejecutar Redis usando la configuración personalizada
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]