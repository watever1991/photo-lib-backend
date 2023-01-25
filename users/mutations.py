import graphene
import graphql_jwt
from .models import CustomUser
from graphene_django import DjangoObjectType
from .password_generator import generate_password
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        try:
            user = CustomUser(
                username=username,
                email=email,
            )
        except Exception as e:
            return CreateUser(success=False, errors=e)
        user.set_password(password)
        user.save()

        return CreateUser(user=user, success=True)


class GetUser(graphene.Mutation):
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        try:
            user = CustomUser.objects.get(pk=id)
        except:
            return GetUser(success=False, errors="Invalid Details")
        return GetUser(user=user, success=True)


class ForgotPasswordMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.String()

    def mutate(self, info, username, email):
        try:
            user = CustomUser.objects.get(username=username, email=email)
        except:
            return ForgotPasswordMutation(success=False, errors="Invalid Details")
        new_password = generate_password(12)
        print(new_password)
        user.set_password(new_password)
        user.save()
        send_mail(
            subject="Your New Password",
            message=f"New Password {new_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email,],
            fail_silently=False
        )
        return ForgotPasswordMutation(user=user, success=True)


class ResetPasswordMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        current_password = graphene.String(required=True)
        new_password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.String()

    @login_required
    def mutate(self, info, id, current_password, new_password):
        user = CustomUser.objects.get(pk=id)
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return ResetPasswordMutation(success=True, errors=None)
        else:
            raise Exception("Current Password Doesnt Match!")
