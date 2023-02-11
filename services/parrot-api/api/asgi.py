import uvicorn
from api.fastapi_app import create_app

uvicorn.run(create_app(), host="127.0.0.1", port=6780)
