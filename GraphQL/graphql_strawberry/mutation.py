import strawberry
from graphql import GraphQLError
from type import User, Post
from data import users, posts

@strawberry.type
class UserMutation:

    @strawberry.mutation
    def create_user(self,name:str,email:str)->User:
        id = len(users) + 1
        user = {
            "id":id,
            "name":name,
            "email":email
        }
        users.append(user)
        return User(**user)

    @strawberry.mutation
    def update_user(self,id:int,name:str|None=None,email:str|None=None)->User:
        user = next((user for user in users if user["id"]==id),None)
        if user is None:
            raise Exception(f"User does not exist with given id: {id}")
        if name:
            user['name']=name
        if email:
            user['email']=email
        return User(**user)

    @strawberry.mutation
    def delete_user(self,id:int)->User:
        user = next((user for user in users if user["id"]==id),None)
        if user is None:
            raise Exception(f"User does not exist with given id: {id}")
        users.remove(user)
        return User(**user)


@strawberry.type
class PostMutation:

    @strawberry.mutation
    def create_post(self,title:str,content:str,author_id:int)->Post:
        author = any(user["id"]==author_id for user in users)
        if not author:
            raise GraphQLError(
                message=f"User not found with id {author_id}.",
                extensions={"code": "NOT_FOUND", "http_status": 404}
            )
        id = len(posts) + 1
        post = {
            "id":id,
            "title":title,
            "content":content,
            "author_id":author_id
        }
        posts.append(post)
        return Post(**post)

    @strawberry.mutation
    def update_post(self,id:int,title:str|None=None,content:str|None=None,author_id:int|None=None)->Post:
        post = next((post for post in posts if post["id"]==id),None)
        if post is None:
            raise Exception(f"Post does not exist with given id: {id}")
        if author_id:
            if not any(user["id"]==author_id for user in users):
                raise Exception(f"Author does not exist with author_id: {author_id}")
            post['author_id']=author_id
        if title:
            post['title']=title
        if content:
            post['content']=content
        return Post(**post)

    @strawberry.mutation
    def delete_post(self,id:int)->Post:
        post = next((post for post in posts if post["id"]==id),None)
        if post is None:
            raise Exception(f"Post does not exist with given id: {id}")
        posts.remove(post)
        return Post(**post)

@strawberry.type
class Mutation(UserMutation,PostMutation):
    pass
    
