import strawberry
from data import posts,users

@strawberry.type
class User:
    id: int
    name: str
    email: str
    @strawberry.field
    def posts(self)->list["Post"]:
        user_posts = (post for post in posts if post["author_id"]==self.id)
        return [Post(**post) for post in user_posts]

@strawberry.type
class Post:
    id: int
    title: str
    content: str
    author_id: int

    @strawberry.field
    def author(self) -> User | None:
        user = next((user for user in users if user["id"]==self.author_id),None)
        if user is None:
            return None

        return User(**user)
    