# hello_world

aplicatie flask minimalista hello_world pregatita pentru container & kubernetes. include endpoint-uri utile, meta-info (instance id, hostname, uptime) si o pagina html simpla. 

## structura proiect
```
hello_world_hw/
- app.py
- requirements.txt
- dockerfile
- k8s/
   - deployment.yaml
   - service.yaml
```

## endpoint-uri
- `/` – json cu info instanta  
- `/healthz` – liveness probe  
- `/readyz` – readiness probe (gata dupa 2 sec)  
- `/echo` – post, intoarce ce primeste  
- `/time` – timp server utc  
- `/html` – pagina html

## rulare rapida (fara build imagine)
```powershell
# cu docker (runtime moby)
docker run --rm -it -p 8000:8000 -v ${PWD}:/app -w /app python:3.12-slim `
  bash -lc "pip install -r requirements.txt && python app.py"

# cu nerdctl (runtime containerd)
nerdctl run --rm -it -p 8000:8000 -v ${PWD}:/app -w /app python:3.12-slim `
  bash -lc "pip install -r requirements.txt && python app.py"
```
acces: [http://localhost:8000/html](http://localhost:8000/html)

## construire imagine si rulare local
```powershell
# build imagine
docker build -t hello_world:1.0 .
# sau
nerdctl build -t hello_world:1.0 .

# run container
docker run --rm -p 8000:8000 --name hello_world hello_world:1.0
```
acces: [http://localhost:8000/](http://localhost:8000/)

## deploy in kubernetes (rancher desktop)
```powershell
kubectl apply -f .\k8s\deployment.yaml
kubectl apply -f .\k8s\service.yaml
kubectl port-forward svc/hello-world 8080:80
```
acces: [http://localhost:8080/html](http://localhost:8080/html)

## personalizare prin variabile de mediu
```powershell
docker run -p 8000:8000 `
  -e APP_NAME=demo `
  -e APP_GREETING="heloou!" `
  hello-world:1.0
```

## cleaning
```powershell
kubectl delete -f .\k8s\service.yaml
kubectl delete -f .\k8s\deployment.yaml
docker rm -f hello-unique
docker rmi hello-flask-unique:1.0
```

