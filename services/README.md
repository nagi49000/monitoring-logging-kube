# A simple fastapi service
This is a service for playing with FastAPI and Docker

### FastAPI app ###

The app is contained wholely in the 'api' directory. This contains unit tests, and a full ymls for a conda environments (a -test.yml for dev, and a -prod.yml for prod). A development environment can be created (and entered) by
```
# in fastapi-docker-kube/services/api/
conda env create -f environment-prod.yml
conda env update -f environment-test.yml --name fastapi_prod_env
conda activate fastapi_prod_env
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

### Docker or Podman ###

All unit tests and image builds can be run straight from the dockerfile
```
# in fastapi-docker-kube/services/
docker build . -t simple-app
```

The app can be run (in a container) using
```
docker run -e LOG_LEVEL=INFO -p 8080:6780 simple-app
```

For using podman, replace 'docker' with 'podman'.

### FastAPI docs ###

Once the app is running, one can interact directly with the endpoints (which should be available at http://localhost:8080). As for all FastAPI apps, there are docs available on the endpoints
*  /openapi.json
*  /docs
*  /redoc