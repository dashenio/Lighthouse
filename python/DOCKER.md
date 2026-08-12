# DOCKER



#### What is a container (docker concept)?

* A way to package application with all the necessary dependencies and configuration
* Portable artifact, easily shared and moved around
* Makes development and deplyoment more efficient



Consists of its own isoltaed enviroment packaged with all need configuration and one command installation.



#### Where do containers live?

In a **container repository**.

&#x09;They can be public (Docker Hub) or private (campany owned)

What are containers made of?

Layers of images

Mostly Linux Base Image because of small size

App Image on top

Intermediary images



docker pull nome\_aplicacao - baixa a imagem mais recente disponível no repositório

docker run nome\_aplicacao - cria o container (se não tiver a image localmente ele baixa a imagem do repositório)

docker pull nome\_aplicacao:9.6 - baixa a versão especificada da imagem

docker ps - ver containers em execução

docker images - mostra todas as imagens baixadas

docker run -d nome - detached

docker stop id\_app

docker start id\_app

docker ps -a - mostra TODOS os  containers

docker logs id\_app - abre os logs do container

docker run -d -pPORT\_HOST:PORT\_container --name novo\_nome\_app - 	atribui um nome personalizado ao container

docker exec -it container\_id ou container\_name /bin/bash - entrar na pasta de arquivos do container

dentro da pasta use **env** para ver a variáveis de ambiente



BUILDAR IMG

docker build -t DOCKER\_USERNAME/getting-started-todo-app .

docker image ls
docker push <DOCKER\_USERNAME>/getting-started-todo-app



Diferença entre Image e Container

Image - the actual package with the configuration

Container - running environment for IMAGE



Docker VS Virtual Machine

Docker need the OS kernel - Linux based dcoker image cant run on Windows OS kernel

Use Docker Desktop to abstract the kernel to make possible for your host to run different docker images



Voce pode ter vários containers rodando ao mesmo tempo o mesmo app mas tem que associar à um port diferente para que não haja conflitos

some-app://localhost:3001



docker run -p6000:6379 - p6000 é o port do host, o que vem depois dos : é o port padrão do app o qual vc está associando ao port do host (seu PC)



PERSIST DATA

