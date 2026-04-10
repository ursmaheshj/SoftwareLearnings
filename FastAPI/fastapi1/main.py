from fastapi import FastAPI
from models import Product

app = FastAPI()

product = [
    Product(id=1,name="laptop",description="acer",price=13433,quantity=2),
    Product(id=2,name="phone",description="mobile",price=10999,quantity=1),
    Product(id=3,name="monitor",description="desktop",price=200000,quantity=3),
] 

@app.get("/")
def greet():
    return "Hi its me"    

@app.get("/product", include_in_schema=False)
def get_all_products():
    return product

@app.get("/product/{id:int}", include_in_schema=False)
def get_product(id: int):
    for p in product:
        if id == p.id:
            return p
    return "Product not found" 

@app.post("/product", include_in_schema=False)
def add_product(p: Product):
    product.append(p)
    return product

@app.put("/product", include_in_schema=False)
def update_product(id: int, p: Product):
    for i in range(len(product)):
        if product[i].id==id:
            product[i]=p
            return "product added success"
    return "product not found"

@app.delete("/product", include_in_schema=False)
def delete_product(id: int):
    for i in range(len(product)):
        if product[i].id==id:
            del product[i]
            return "product deleted"
        
    return "product not found"