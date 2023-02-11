import logging
import os
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from fluent.handler import (
    FluentHandler,
    FluentRecordFormatter
)


class HelloWorldResponse(BaseModel):
    message: str


class ParrotRequestParams(BaseModel):
    n_repeat: int
    sep: str
    parrot_str: str


class ParrotRequest(BaseModel):
    header: str
    parrot_request: ParrotRequestParams


class ParrotBackResponseResults(BaseModel):
    time: str
    parrot: str


class ParrotBackResponse(BaseModel):
    header: str
    results: ParrotBackResponseResults


def get_gunicorn_logger(name="gunicorn.error", app_name="my app"):
    # dirty way of wiring into the gunicorn logger
    logger = logging.getLogger(name)

    # set up a Fluent handler for sending logs to fluent
    fluent_host = os.getenv("FLUENT_HOST", "localhost")
    fluent_port = int(os.getenv("FLUENT_PORT", "24224"))

    fluent_format = {
        "host": "%(hostname)s",
        "where": "%(module)s.%(funcName)s",
        "type": "%(levelname)s",
        "stack_trace": "%(exc_text)s"
    }
    h = FluentHandler(app_name, host=fluent_host, port=fluent_port)
    h.setFormatter(FluentRecordFormatter(fluent_format))
    logger.addHandler(h)

    # overwrite the root logger handlers with the gunicorn logger handlers,
    # so that root logger messages get sent to gunicorn and fluent
    root_logger = logging.getLogger()
    root_logger.handlers = logger.handlers
    root_logger.setLevel(logger.level)
    logger.info(f"Fluent logging to {fluent_host} on port {fluent_port}")
    return logger


def create_app(logger_name="gunicorn.error"):
    app_name = os.getenv("APP_NAME", "simple test app")
    root_path = os.getenv("ROOT_PATH", None)
    logger = get_gunicorn_logger(name=logger_name, app_name=app_name)
    logger.info(f"app name = {app_name} with api root path {root_path}")
    app = FastAPI(title=app_name, root_path=root_path)

    @ app.get("/hello_world", response_model=HelloWorldResponse)
    async def hello_world():
        logger.debug("/hello_world")
        return {"message": "Hello World"}

    @ app.post("/parrot_back", response_model=ParrotBackResponse)
    async def parrot_back(p: ParrotRequest):
        p_dict = p.dict()
        logger.debug(f"/parrot_back: {p_dict}")
        # get the params for making a parrot back message
        q = p_dict["parrot_request"]
        parrot_message = q["sep"].join([q["parrot_str"]] * q["n_repeat"])
        r_dict = {
            "header": p_dict["header"],
            "results": {
                "time": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "parrot": f"parrot back {parrot_message}"
            }
        }
        return r_dict

    return app
