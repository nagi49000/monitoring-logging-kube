# A simple fastapi service
This is a service for playing with FastAPI and Docker

### FastAPI app ###

The app is contained wholely in the 'api' directory. This contains unit tests, and a full ymls for a conda environments (a -test.yml for dev, and a -prod.yml for prod). A development environment can be created (and entered) by
```
# in fastapi-docker-kube/services/api/
conda env create -f environment-test.yml
conda activate fastapi_play_env
```

The unit tests can be run using pytest (from the api directory).
```
# in fastapi-docker-kube/services/api/
python -m pytest
```

The app can be brought up in a development server by running
```
# in fastapi-docker-kube/services/api/
python asgi.py
```

### Docker ###

The docker setup consists of:

*  docker-compose.yml
*  Dockerfile-prod
*  Dockerfile-test

Unit tests and builds can be run using
```
# in fastapi-docker-kube/services/
docker-compose build
```
and the app can be run (in a container) using
```
# in fastapi-docker-kube/services/
docker-compose up
```

### Using Podman instead of Docker ###

Instead of using the docker-compose, one can run the podman commands directly (as though one were running the docker commands directly)

Unit tests and builds can be run using
```
# in fastapi-docker-kube/services/
podman build -f Dockerfile-test . -t fastapi-docker-kube-test
podman build -f Dockerfile-prod . -t fastapi-docker-kube-prod
```
and the app can be run (in a container) using
```
podman run -p 8080:6780 fastapi-docker-kube-prod:latest
```

### FastAPI docs ###

Once the app is running, one can interact directly with the endpoints (which should be available at http://localhost:8080). As for all FastAPI apps, there are docs available on the endpoints
*  /openapi.json
*  /docs
*  /redocvirtual