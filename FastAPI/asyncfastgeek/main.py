from fastapi import FastAPI,Request
from asyncfastgeek.routers import router as user_router
from asyncfastgeek.routers import profilerouter
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

app = FastAPI(
    title="My FastAPI Learning",
    description="This project contains fastapi learning code",
    version="0.2.0",
    contact={
        "name":"Mahesh",
        "url":"http://mahesh.com",
        "email":"mahesh@example.com"
    },
    license_info={
        "name":"MIT license",
        "url":"http://mitlicense.example.com"
    }
)

load_dotenv()
app.include_router(user_router, prefix="/api/users",tags=["users"])
app.include_router(profilerouter, prefix="/api/profile",tags=["profile"])

@app.middleware("http")
async def custom_middleware(request: Request, next_call):
    print("Middleware: Before handling request")
    response = await next_call(request)
    print("Middleware: After handling request")
    return response

app.mount("/static", StaticFiles(directory="static"),name="static")
# Using absolute path for staticfiles dir
# base_dir = Path(__file__).resolve().parent
# app.mount("/static", StaticFiles(directory=base_dir / "static"), name="static")