from fastapi import FastAPI
import datetime
import logging
import os
from pydantic import BaseModel


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


def get_gunicorn_logger(name="gunicorn.error"):
    logger = logging.getLogger(name)  # dirty way of wiring into the gunicorn logger
    # overwrite the root logger with the gunicorn logger
    root_logger = logging.getLogger()
    root_logger.handlers = logger.handlers
    root_logger.setLevel(logger.level)
    return logger


def create_app(logger_name="gunicorn.error"):
    logger = get_gunicorn_logger(name=logger_name)
    app_name = os.getenv("APP_NAME", "simple test app")
    root_path = os.getenv("ROOT_PATH", None)
    app = FastAPI(title=app_name, root_path=root_path)

    @app.get("/hello_world", response_model=HelloWorldResponse)
    async def hello_world():
        logger.debug('/hello_world')
        return {"message": "Hello World"}

    @app.post("/parrot_back", response_model=ParrotBackResponse)
    async def parrot_back(p: ParrotRequest):
        p_dict = p.dict()
        logger.debug('/parrot_back: '+str(p_dict))
        params = p_dict['parrot_request']
        r_dict = {'header': p_dict['header'],
                  'results': {'time': datetime.datetime.utcnow().isoformat(timespec='seconds')+'Z',
                              'parrot': 'parrot back ' + params['sep'].join([params['parrot_str']]*params['n_repeat'])
                              }
                  }
        return r_dict

    return app
