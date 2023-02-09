FROM continuumio/miniconda3:latest AS builder

ENV APP_HOME=/app
WORKDIR ${APP_HOME}
COPY api ./
RUN conda env update --file environment-prod.yml --name base --prune && \
    groupadd --system app && \
    useradd -g app --system app && \
    chown -R app:app ${APP_HOME} && \
    chmod -R 755 ${APP_HOME}

FROM builder AS tester

RUN conda env update --file environment-test.yml --name base && \
    python -m flake8 ./ && \
    python -m pytest --cov=./api

FROM builder

ENV LOG_LEVEL INFO
# exec in so that OS signals are picked up in the running container by docker
CMD exec gunicorn -k uvicorn.workers.UvicornWorker api.api_app:app --bind 0.0.0.0:6780 --log-level $LOG_LEVEL