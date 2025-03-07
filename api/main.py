from fastapi import FastAPI
from api.models.models import Product  # Import the Product model

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    product = Product(product_id=product_id, name="Example Product", price=9.99)
    return product