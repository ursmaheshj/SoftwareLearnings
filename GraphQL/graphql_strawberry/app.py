from fastapi import FastAPI
from schema import graphql_router

app = FastAPI(
    title="Fastapi app for Graphql with Strawberry",
    version="1.0.0"
)

app.include_router(graphql_router,prefix="/graphql")