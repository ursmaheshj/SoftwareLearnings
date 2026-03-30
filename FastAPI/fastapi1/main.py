from fastapi import FastAPI
from models import Product

app = FastAPI()

product = [
    Product(1,"laptop","acer",13433,2),
    Product(2,"smartphone","samung",10999,1),
    Product(3,"desktop","ant",200000,5)
] 

@app.get("/")
def greet():
    return "Hi its me"

@app.get("/product")
def products():
    return product

@app.get("/product/<id:int>")
def products(id):
    print("mj",id)
    return product[id]