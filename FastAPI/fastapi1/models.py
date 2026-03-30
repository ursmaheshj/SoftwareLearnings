class Product():
    id: int
    name: str
    description: str
    price: int
    quantity: int

    def __init__(self,id,name,description,price,quantity):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity