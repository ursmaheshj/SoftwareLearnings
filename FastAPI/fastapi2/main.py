from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from models import Product
from database import db_session,engine
import db_models

app = FastAPI()

db_models.Base.metadata.create_all(bind=engine)

products = [
    Product(id=1,name="laptop",description="acer",price=13433,quantity=2),
    Product(id=2,name="phone",description="mobile",price=10999,quantity=1),
    Product(id=3,name="monitor",description="desktop",price=200000,quantity=3),
] 

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = db_session()
    count = db.query(db_models.Product).count()
    if count==0:
        for product in products:
            db.add(db_models.Product(**product.model_dump()))
    db.commit()

init_db()

@app.get("/")
def greet():
    return "Hi its me"    

@app.get("/product")
def get_all_products(db: Session = Depends(get_db)):
    p = db.query(db_models.Product).all()
    return p

@app.get("/product/{id:int}")
def get_product(id: int,db: Session = Depends(get_db)):
    p = db.query(db_models.Product).filter(db_models.Product.id==id).first()
    if p:
        return p
    return "Product not found" 

@app.post("/product")
def add_product(p: Product,db: Session = Depends(get_db)):
    db.add(db_models.Product(**p.model_dump()))
    db.commit()
    return products

@app.put("/product")
def update_product(id: int, p: Product, db:Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
            db_product.name = p.name if p.name else db_product.name
            db_product.description = p.description if p.description else db_product.description
            db_product.quantity = p.quantity
            db_product.price = p.price
            db.commit()
            return "product updated success"
    return "product not found"

@app.delete("/product")
def delete_product(id: int, db:Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted successfully"
        
    return "product not found"