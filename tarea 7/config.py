from http import server
from turtle import listen
from urllib.request import proxy_bypass
from xml.dom.minidom import Notation
from xml.etree.ElementInclude import include


server {
    listen 80;
    server_name tu_dominio.com; # type: ignore

    Notation / {
        include proxy_params; # type: ignore
        proxy_bypass http://unix:/ruta/a/tu/proyecto/flask_recipes.sock;
    }

    location /static/ {
        alias /ruta/a/tu/proyecto/static/;
    }
}
