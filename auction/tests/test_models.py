from django.test import TestCase
from auction.models import Post, FileUpload
from django.core.files.uploadedfile import SimpleUploadedFile


class PostTest(TestCase):
    def setUp(self) -> None:
        self.image = SimpleUploadedFile(name='test_image.png', content=open('auction/tests/test_image.png', 'rb').read(), content_type='image/png')
        self.check_post = Post(title="MyPost", price=22.60, creator="John Doe", banner=self.image)

    def test_post_return(self):
        """str function for Post should return the title"""
        self.assertEquals(str(self.check_post), "MyPost")

    def test_banner_upload(self):
        """banner name should be test_image.png"""
        self.assertTrue(self.check_post.banner)
        self.assertEqual(self.check_post.banner.name.split("/")[0], 'test_image.png')
        self.assertEqual(self.check_post.banner.size, self.image.size)


class FileUploadTest(TestCase):
    def setUp(self):
        self.image = SimpleUploadedFile(name='test_image.png', content=open('auction/tests/test_image.png', 'rb').read(), content_type='image/png')
        self.mymodel = FileUpload.objects.create(file_name="mike", image_field=self.image)

    def test_image_upload(self):
        """Testing the image field for each post"""
        self.assertTrue(self.mymodel.image_field)
        self.assertTrue('media/test_image' in self.mymodel.image_field.name)
        self.assertEqual(self.mymodel.image_field.size, self.image.size)
        
        