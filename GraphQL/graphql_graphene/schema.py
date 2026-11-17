import graphene

from query import Query
from mutation import CreateUser, UpdateUser, DeleteUser


class MutationRoot(graphene.ObjectType):

    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = graphene.Schema(
    query=Query,
    mutation=MutationRoot
)
