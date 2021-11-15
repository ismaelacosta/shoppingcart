from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

from api.routes import carrito_routes

"""class Item(BaseModel):
    name : str
    description : Optional[str] = None
    price : float
    tax : Optional[float] = None
    #Declarar ejemplos de nuestro esquema
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
                }
            }
            """


app = FastAPI()

app.include_router(carrito_routes.router)


"""@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(item : Item):
    return item"""