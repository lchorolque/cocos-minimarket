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
 
