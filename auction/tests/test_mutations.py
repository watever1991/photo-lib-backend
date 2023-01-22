from graphene_django.utils.testing import GraphQLTestCase
from auction.models import Post, FileUpload
from django.core.files.uploadedfile import SimpleUploadedFile
from graphene_file_upload.django.testing import GraphQLFileUploadTestCase


class PostMutationTest(GraphQLFileUploadTestCase):
    def test_post_creation_mutation(self):
        test_file = SimpleUploadedFile(name='test_image.png', content="test_image.png".encode("utf-8"))
           
        response = self.file_query(
            """
            mutation postMutation($title: String!, $price: Float!, $creator: String!, $banner: Upload) {
                createPost(title: $title, price: $price, creator: $creator, banner: $banner) {
                    post {
                        id
                        title
                        price
                        creator
                    }
                    success
                    errors
                }
            }
            """,
            op_name="postMutation",
            variables={
                "title": "The Great Gatsby",
                "price": 44.78,
                "creator": "Aprotim",
            },
            files={"banner": test_file}
        )

        self.assertResponseNoErrors(response)


class PostFileUploadMutationTest(GraphQLFileUploadTestCase):
    def setUp(self) -> None:
        Post(
            title="The Great Gatsby",
            price=44.78,
            creator="Aprotim",
            banner=None
        )
        self.test_file = SimpleUploadedFile(name='test_image.png', content="test_image.png".encode("utf-8"))

    def test_post_file_upload(self):
        response = self.file_query(
            """
            mutation postFileUploadMutation($id: ID!, $fileName: String!, $imageField: Upload) {
                postFileUpload(id: $id, fileName: $fileName, imageField: $imageField) {
                    post {
                        id
                        title
                        price
                        creator
                    }
                }
            }
            """,
            op_name="postFileUploadMutation",
            variables={
                "id": 1,
                "fileName": "masterfile"
            },
            files={"imageField": self.test_file}
        )

        self.assertResponseNoErrors(response)


class PostDataMutationTest(GraphQLTestCase):
    image = SimpleUploadedFile(name='test_image.png', content=open('auction/tests/test_image.png', 'rb').read(),\
            content_type='image/png')
    def setUp(self) -> None:
        Post(
            title="The Great Gatsby",
            price=44.78,
            creator="Aprotim",
            banner=self.image
        ),
        FileUpload(
            pk=1,
            file_name="johnfile",
            image_field=self.image
        )

    def test_post_data_mutation(self):
        response = self.query(
            """
            mutation postDataMutation($id: ID!) {
                getPost(id: $id) {
                    post {
                        id
                        title
                        price
                        creator
                    }
                }
            }
            """,
            operation_name="postDataMutation",
            variables={"id": 1}
        )

        self.assertResponseNoErrors(response)
