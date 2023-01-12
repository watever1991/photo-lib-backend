from django.contrib import admin
from .models import CustomUser
from django.apps import apps
from auction.models import FileUpload, Post
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(FileUpload)
admin.site.register(Post)