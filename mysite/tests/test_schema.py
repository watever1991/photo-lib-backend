from users.models import CustomUser
from graphql_jwt.testcases import JSONWebTokenTestCase


class TestUserQuery(JSONWebTokenTestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.client.authenticate(self.user)
        self.new_user = CustomUser.objects.create_user(
            username='staffuser',
            email='testuser@example.com',
            password='testpassword123',
            is_active=True
        )
        self.client.authenticate(self.new_user)

    def test_user_query(self):
        query = """
            query {
                users {
                    id
                    username
                    email
                }
            }
            """

        self.client.execute(query)

    def test_me_query(self):
        query = """
            query {
                me {
                    id
                    username
                    email
                }
            }
            """

        self.client.execute(query)