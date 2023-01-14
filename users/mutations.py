import graphene
from .models import CustomUser
from graphene_django import DjangoObjectType
from .password_generator import generate_password
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser


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
