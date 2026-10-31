
from graphene import String, Mutation, Field
from data import users
from type import User


class CreateUser(Mutation):

    class Arguments:
        id = String(required=True)
        name = String(required=True)
        email = String(required=True)
        age = String(required=True)
        password = String(required=True)

    user = Field(User)

    def mutate(root, info, id, name, email, age, password):

        new_user = {
            "id": id,
            "name": name,
            "email": email,
            "age": age,
            "password": password
        }

        users.append(new_user)

        return CreateUser(
            user=User(**new_user)
        )


class UpdateUser(Mutation):

    class Arguments:
        id = String(required=True)
        name = String()
        email = String()
        age = String()
        password = String()

    user = Field(User)

    def mutate(root, info, id, **kwargs):

        old_user = next(
            (user for user in users if user.get("id") == id),
            None
        )

        if old_user is None:
            return UpdateUser(user=None)

        # Update only provided fields
        for key, value in kwargs.items():
            if value is not None:
                old_user[key] = value

        return UpdateUser(
            user=User(**old_user)
        )


class DeleteUser(Mutation):
    class Arguments:
        id = String(required=True)

    user = Field(User)

    def mutate(root, info, id):

        old_user = next(
            (user for user in users if user.get("id") == id),
            None
        )

        if old_user is None:
            return DeleteUser(user=None)

        users.remove(old_user)

        return DeleteUser(
            user=User(**old_user)
        )
