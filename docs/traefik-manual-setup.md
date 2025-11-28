# Intro
If you're using Traefik as your reverse proxy in your docker setup, you might want to use it as well to centrally serve the ```/robots.txt``` for all your Traefik fronted services.

This can be achieved by configuring a single lightweight service to service static files and defining a high priority Traefik HTTP Router rule.

# Setup
Define a single service to serve the one robots.txt to rule them all. I'm using a lean nginx:alpine docker image in this example:

```
services:
  robots:
    image: nginx:alpine
    container_name: robots-server
    volumes:
      - ./static/:/usr/share/nginx/html/:ro
    labels:
      - "traefik.enable=true"
      # Router for all /robots.txt requests
      - "traefik.http.routers.robots.rule=Path(`/robots.txt`)"
      - "traefik.http.routers.robots.entrypoints=web,websecure"
      - "traefik.http.routers.robots.priority=3000"
      - "traefik.http.routers.robots.service=robots"
      - "traefik.http.routers.robots.tls.certresolver=letsencrypt"
      - "traefik.http.services.robots.loadbalancer.server.port=80"
    networks:
      - external_network

networks:
  external_network:
     name: traefik_external_network
     external: true
```

The Traefik HTTP Routers rule explicitly does not contain a Hostname. Traefik will print a warning about this for the TLS setup but it will work. The high priority of 3000 should ensure this rule is evaluated first for incoming requests.

Place your robots.txt in the local `./static/` directory and NGINX will serve it for all services behind your Traefik proxy.
