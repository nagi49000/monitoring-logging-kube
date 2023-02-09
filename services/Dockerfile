FROM continuumio/miniconda3:latest

WORKDIR /app
COPY api ./
RUN conda env update --file environment-prod.yml --name base && \
    conda env update --file environment-test.yml --name base && \
    python -m pytest --cov=./api

FROM continuumio/miniconda3:latest

ENV APP_HOME=/app
WORKDIR ${APP_HOME}
COPY api ./
RUN conda env update --file environment-prod.yml --name base --prune && \
    groupadd --system app && \
    useradd -g app --system app && \
    chown -R app:app ${APP_HOME} && \
    chmod -R 755 ${APP_HOME}
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "api.api_app:app", "--bind", "0.0.0.0:6780", "--log-level", "DEBUG"]