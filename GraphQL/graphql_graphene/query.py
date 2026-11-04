
import graphene
from data import users
from type import User


class Query(graphene.ObjectType):

    get_user = graphene.Field(
        User,
        id=graphene.ID(required=True)
    )

    get_users = graphene.List(User)

    def resolve_get_user(root, info, id):
        return next((user for user in users if str(user.get("id")) == str(id)),None)

    def resolve_get_users(root, info):
        return users
