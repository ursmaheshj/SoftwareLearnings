
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp,make_playground_handler

from schema import schema


app = FastAPI(
    title="FastAPI GraphQL API",
    description="GraphQL API using FastAPI and Graphene(Query and Mutation)",
    version="1.0.0"
)


# GraphQL endpoint
app.mount(
    "/graphql",
    GraphQLApp(
        schema=schema,
        on_get=make_playground_handler(
                    playground_options={
                        "subscriptionEndpoint": "/graphql"
                    }
                )
    )
)


@app.get("/")
async def home():
    return {
        "message": "FastAPI + Graphene API is running",
        "graphql_endpoint": "/graphql"
    }

