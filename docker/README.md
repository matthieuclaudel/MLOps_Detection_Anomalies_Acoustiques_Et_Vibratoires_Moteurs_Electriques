## Ce répertoire contient les containers docker pour chaque brique de la solution: 
1- Network bridge
```shell
docker network create bridge_test_container
```
2- Model
```shell
docker build -t adrien157/model -f docker/dockerfile.app_model .
docker push adrien157/model:latest
docker run --rm --name model --env-file .env -p 8000:8000 --network bridge_test_container adrien157/model:latest
```
3- Le premier docker file dockerfile.app_simu et une application qui permet de simuler les machines. Il suffit d'indiquer dans les environnements variables l'aPI URL, le user et le mot de passe.
```shell
docker build -t adrien157/simulation_request_model -f docker/dockerfile.app_simu .
docker push adrien157/simulation_request_model:latest
docker run --rm --name simu_request --env-file .env --network bridge_test_container adrien157/simulation_request_model:latest
```