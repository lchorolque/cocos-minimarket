# COCOs MiniMarket - Backend Project
 
## Introduccion
 
COCOs MiniMarket es una api backend desarrollada en base a las especificación del desafió Minimart API de Arizon
 
A continuacion se especifican los pasos a seguir para proceder con su configuración en un entorno de desarrollo.
 
## 0 - Requisitos
 
COCOs MiniMarket Backend Project necesita de los siguientes requerimientos de software para poder utilizarse:
 
- Sistema Operativo Linux - Distribuciones Ubuntu / Debian / CentOS
- Sistema Operativo macOS - Sierra
- Docker
- Docker Compose
- Direnv
 
## 1 - Clonacion
 
Para ejecutar el proceso de clonacion se utiliza el siguiente comando que descarga el Backend Project desde el repositorio GitHub:
 
```bash
git clone git@github.com:lchorolque/cocos-minimarket.git
```
 
## 2 - Buildeo
 
Para buildear el Backend Project utilizando el engine de Docker se utiliza el siguiente conjunto de comandos:
 
1 - Ubicarse en el proyecto COCOs MiniMarket Backend
```bash
cd cocos-minimarket
``` 
2 - Permitir uso de direnv
```bash
direnv allow
``` 
3 - Ubicarse en la raiz de configuracion Docker del proyecto
```bash
cd docker
```
4 - Buildear el proyecto con Docker Compose
```bash
docker-compose build
```
5 - Levantar el proyecto con Docker Compose
```bash
docker-compose up
```
 
## 3 - Instanciación
 
Luego de tener el proyecto construido y levantado por Docker, correremos el comando de inicialización para  instalar las migraciones y los fixtures de datos.

1 - Ubicarse en el proyecto COCOs MiniMarket Backend
```bash
cd cocos-minimarket
``` 
2 - Ubicarse en la raiz de configuracion Docker del proyecto
```bash
cd docker
```
3 - Corremos el comando de inicialización
```bash
sh init_service.sh
```

## 4 - Crear usuario

Luego de tener el proyecto inicializado, crearemos un usuario para poder interactuar con la API.

1 - Ubicarse en el proyecto COCOs MiniMarket Backend
```bash
cd cocos-minimarket
``` 
2 - Ubicarse en la raiz de configuracion Docker del proyecto
```bash
cd docker
```
3 - Ingresaremos al bash del backend
```bash
sh bash.sh
```
4 - correremos el siguiente comando y seguiremos los pasos
```bash
./manage.py createsuperuser
```
