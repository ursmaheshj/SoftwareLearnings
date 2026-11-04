import strawberry
from type import User, Post
from data import users,posts

@strawberry.type
class Query:

    @strawberry.field
    def get_users(self) -> list[User]:
        return [User(**user) for user in users]

    @strawberry.field
    def get_user(self,id: int) -> User:
        user = next((user for user in users if user["id"]==id),None)
        if user is None:
            return None
        return User(**user)

    @strawberry.field
    def get_posts(self) -> list[Post]:
        return [Post(**post) for post in posts]

    @strawberry.field
    def get_post(self,id: int)-> Post:
        post = next((post for post in posts if post["id"]==id),None)
        return Post(**post)