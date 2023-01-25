import graphene
import graphql_jwt
from users.mutations import CreateUser, UserType, CustomUser, GetUser, ForgotPasswordMutation,\
    ResetPasswordMutation, ObtainJSONWebToken
from auction.mutations import PostMutation, PostDataMutation, PostFileUploadMutation


class AuthMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    get_user = GetUser.Field()
    change_password_if_forgotten = ForgotPasswordMutation.Field()
    reset_password = ResetPasswordMutation.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return CustomUser.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user


class Mutation(AuthMutation, graphene.ObjectType):
    create_post = PostMutation.Field()
    post_file_upload = PostFileUploadMutation.Field()
    get_post = PostDataMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)