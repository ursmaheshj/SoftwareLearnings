from fastapi import APIRouter, HTTPException, status, Depends
from fastapi import Response, Cookie, Request, Header
from fastapi import BackgroundTasks, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
from asyncfastgeek.db_models import create_tables
from asyncfastgeek.services import create_user,list_users,get_user,update_users,delete_user
from asyncfastgeek.schemas import CreateUSer, OutUser, UpdateUser
from asyncfastgeek.dependencies import verify_token
import time,os

router = APIRouter()
profilerouter = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/createdb")
async def createdb():
    await create_tables()
    return {"msg":"tables created"}

@router.post("/")
async def createuser(createuser: CreateUSer):
    await create_user(createuser)
    return {"msg":"User created"}

@router.get("/{user_id}",response_model=OutUser)
async def getuser(user_id: int):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/",response_model=list[OutUser])
async def listusers():
    users = await list_users()
    return users

@router.patch("/{user_id}",response_model=CreateUSer)
async def updateuser(user_id: int, newdata: UpdateUser):
    user = await update_users(user_id, newdata)
    return user

@router.delete("/{user_id}")
async def deleteuser(user_id: int):
    await delete_user(user_id)
    return {"msg":"User deleted"}

@router.get("/search")
async def all_users(userid: int, q: str=None):
    return {
        "userid": userid,
        "q": f"searched for {q}"
    }

@profilerouter.get("/profile")
async def get_profile(token: str = Depends(verify_token)):
    return {"msg":"Access granted", "profile":"FastAPI application"}

@profilerouter.get("/setcookie")
async def set_cookie(response: Response):
    response.set_cookie(
        key="ex_cookie",
        value="dsfa sdhjfas kjsdhf",
        httponly=True,
        max_age=5,
        samesite="lax"
    )
    return {"msg":"cookie set!"}

@profilerouter.get("/getcookie")
async def get_cookie(ex_cookie: Annotated[str | None, Cookie()] = None):
    if ex_cookie:
        return {"msg":f"cookie available: {ex_cookie}"}
    return {"msg":"No cookie found"}

@profilerouter.get("/getcookie2")
async def get_cookie2(request: Request):
    cookie = request.cookies.get("ex_cookie")
    if cookie:
        return {"msg":f"cookie available: {cookie}"}
    return {"msg":"No cookie found"}

@profilerouter.get("/readheader")
async def read_header(x_token: Annotated[str | None, Header()]=None,
                      user_agent: Annotated[str | None, Header()]= None):
    return {"user_agent": user_agent, "x_token": x_token}

@profilerouter.get("/setheader")
async def set_header(response: Response):
    response.headers["X-custom-header"] = "Custom header set on response"
    return {"msg":"header set successfully"}

@profilerouter.get("/checkmiddleware")
async def check_middleware():
    print("Inside function")
    return {"msg":"Middleware working"}

data = ["Mahesh", "Jadhav", "Hnagar", "india"] #example data

@profilerouter.get("/index",response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request,
                                      name="index.html",
                                      context={"data":data})


def send_mail(email: str):
    for i in range(5):
            print(f"sending mail to: {email}")
            time.sleep(1)

@profilerouter.get("/backgroundtask")
async def backgroundtask(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_mail,email)
    return {"msg":f"Email has been sent to:{email}"}

@profilerouter.post("/loginform")
async def login_form(name: Annotated[str, Form(min_length=3)],
                     password: Annotated[str, Form(max_length=20)] = ""): #name required but pass will have default ""
    return {"msg":"User provided details",
            "name":name,
            "password":password}

@profilerouter.post("/fileform")
async def file_loginform(desc: str,file: Annotated[UploadFile, File()]):
    return {"desc":desc, "filename": file.filename, "size":file.size}

@profilerouter.get("/envvars")
async def env_vars():
    db_user = os.getenv("DB_USERNAME")
    db_pass = os.getenv("DB_PASSWORD")
    return {"db_username":db_user,"db_password":db_pass}