from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    price = models.FloatField(max_length=100, null=True, blank=True)
    creator = models.CharField(max_length=200, null=True, blank=True)
    banner = models.ImageField(upload_to="media", null=True, blank=True)
    banner_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

class FileUpload(models.Model):
    relation = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="post_files")
    file_name = models.CharField(max_length=250)
    image_field = models.ImageField(upload_to="media", default=None)
    image_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.file_name
