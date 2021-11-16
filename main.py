from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

from api.routes import carrito_routes

app = FastAPI()

app.include_router(carrito_routes.router)
