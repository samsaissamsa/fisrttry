from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr

from database import collection, user_collection
from schemas import list_serial  
from item import Item
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from bson import ObjectId

from utilis import hash_password, verify_password, create_access_token
from user import User, UserOut, Token

from jose import jwt , JWTError


app = FastAPI()

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id == None:
            raise HTTPException(status_code=401, detail="unauth")
        return user_collection.find_one({"_id": ObjectId(user_id)})
    except JWTError:
        raise HTTPException(status_code=401, detail="unauth")

@app.get("/items")
def get_items():
    items = list_serial(collection.find())
    return items

@app.post("/item")
def create_item(item: Item):
    result = collection.insert_one(dict(item))
    return item

@app.put("/item/{item_id}")
def update_item(item_id: str, item: Item):
    result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": dict(item)})
    return item

@app.post("/register")
def register(user: User) -> UserOut:
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    user_data = {"email": user.email, "password": hashed_password}
    result = user_collection.insert_one(user_data)
    
    return UserOut(email=user.email, id=str(result.inserted_id))

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token :
    db_user = user_collection.find_one({"email": form_data.username})


    if not db_user or not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(db_user["_id"])})
    return Token(access_token=access_token, token_type="bearer")

@app.get("/me")
def read_data_me(current_user: dict = Depends(get_current_user)):
    return UserOut(id=str(current_user["_id"]), email=current_user["email"])







# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# uri = "mongodb+srv://azharinmdb: azharinmdb07@cluster0.utgahb8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)





#class Item(BaseModel):
#   name: str
#    description: str = None
#    price: float
#    tax: float = None
#    tags: list[str] = []
#     out_of_stock: bool = False

# class UserOut(BaseModel):
#     username: str
#     name: str
#     surname: str = None
#     email: EmailStr

# class UserIn(UserOut):
#     password: str

# @app.get("/items")
# def get_items():
#     return {"items": []}

# @app.post("/item")
# def create_item(item: Item):
#     if item.name == "":
#         raise HTTPException(status_code = 400, detail = "Name is required")
#     if item.price == 0:
#         raise HTTPException(status_code = 400, detail = "Price cannot be zero")
#     return item

# @app.post("/user")
# def create(user: UserIn) -> UserOut:
#     return user
