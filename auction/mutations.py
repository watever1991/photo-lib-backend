import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from .models import FileUpload, Post
from mysite import settings


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class FileUploadType(DjangoObjectType):
    class Meta:
        model = FileUpload


class PostMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        price = graphene.Float(required=True)
        creator = graphene.String(required=True)
        banner = Upload()

    post = graphene.Field(PostType)
    success = graphene.Boolean()
    errors = graphene.String()
    
    def mutate(self, info, title, price, creator, banner=None):
        if banner._name.split(".")[1] not in ["jpg", "png", "jpeg"]:
            return PostMutation(success=False, errors="Invalid Image Type")
        try:
            post = Post.objects.create(title=title, price=price, creator=creator, banner=banner)
        except:
            return PostMutation(success=False, errors="Invalid Data Provided")
        post.save()
        if settings.DEBUG:
            post.banner_url = info.context.build_absolute_uri(post.banner.url)[21:]
        else:
            post.banner_url = info.context.build_absolute_uri(post.banner.url)[26:]
        post.save()
        return PostMutation(post=post, success=True)


class PostFileUploadMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        file_name = graphene.String()
        image_field = Upload()
    
    post = graphene.Field(PostType)
    post_files = graphene.List(FileUploadType)
    success = graphene.Boolean()
    errors = graphene.String()

    def mutate(self, info, id, file_name, image_field=None):
        if image_field._name.split(".")[1] not in ["jpg", "png", "jpeg"]:
            return PostFileUploadMutation(success=False, errors="Invalid Image Type")
        try:
            post = Post.objects.get(pk=id)
        except:
            return PostFileUploadMutation(success=False, errors="Invalid ID")
        new_file_data = FileUpload.objects.create(file_name=file_name, image_field=image_field)
        new_file_data.save()
        if settings.DEBUG:
            new_file_data.image_url = info.context.build_absolute_uri(new_file_data.image_field.url)[21:]
        else:
            new_file_data.image_url = info.context.build_absolute_uri(new_file_data.image_field.url)[26:]
        new_file_data.save()
        post.post_files.add(new_file_data)
        post.save()
        return PostFileUploadMutation(post=post, success=True, post_files=post.post_files.all())


class PostDataMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    post = graphene.Field(PostType)
    post_files = graphene.List(FileUploadType)
    success = graphene.Boolean()
    errors = graphene.String()

    def mutate(self, info, id):
        try:
            post = Post.objects.get(pk=id)
        except:
            return PostDataMutation(success=False, errors="Invalid ID")
        return PostDataMutation(post=post, success=True, post_files=post.post_files.all())
