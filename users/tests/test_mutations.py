from graphene_django.utils.testing import GraphQLTestCase
from users.models import CustomUser


class CreateUserTest(GraphQLTestCase):
    def test_user_creation_mutation(self):
        response = self.query(
            """
            mutation createUser($email: String!, $password: String!, $username: String!) {
                createUser(email: $email, password: $password, username: $username) {
                    user {
                        id
                        username
                        email
                    }
                }
            }
            """,
            operation_name="createUser",
            variables={
                "email": "aglida1370@gmail.com", 
                "username": "Monire91", 
                "password": "monire123"
            }
        )

        self.assertResponseNoErrors(response)


class GetUserTest(GraphQLTestCase):
    def setUp(self) -> None:
        CustomUser(
            username="monire91",
            password="monire123",
            email="aglida1370@gmail.com"
        )
        
    def test_get_user_mutation(self):
        response = self.query(
            """
            mutation getUser($id: ID!){
                getUser(id: $id){
                    user {
                        id
                        username
                        email
                    }
                }
            }
            """,
            operation_name="getUser",
            variables={"id": 1}
        )

        self.assertResponseNoErrors(response)
                

class ForgotPasswordMutationTest(GraphQLTestCase):
    def setUp(self) -> None:
        CustomUser(
            username="monire91",
            password="monire123",
            email="aprotim1999@gmail.com"
        )
    
    def test_forget_password_mutation(self):
        response = self.query(
            """
            mutation forgetPasswordMutation($username: String!, $email: String!) {
                changePasswordIfForgotten(username: $username, email: $email) {
                    user {
                        email
                    }
                }
            }
            """,
            operation_name="forgetPasswordMutation",
            variables={
                "username": "monire91",
                "email": "aprotim1999@gmail.com",
            }
        )

        self.assertResponseNoErrors(response)


