from django.test import TestCase
import json
from .models import ActivityVO, User

# from django.urls import reverse
# from django.http.cookie import SimpleCookie

#  lient.cookies is an instance of http.cookies.SimpleCookie


# Create your tests here.
class UsersApiTest(TestCase):
    def setUp(self):
        self.activity = ActivityVO.objects.create(name="Test Activity", id=1)
        self.friend = User.objects.create(
            id=3,
            username="TestFriend",
            first_name="Test",
            last_name="friend",
            email="testfriendemail@gmail.com",
            profile_description="This is a description",
            profile_photo="",
            city="Kalamazoo",
            state="MI",
        )
        self.user = User.objects.create(
            id=2,
            username="TestUser",
            password="password",
            first_name="Test",
            last_name="User",
            email="testemail@gmail.com",
            profile_description="This is a description",
            profile_photo="",
            city="Kalamazoo",
            state="MI",
        )

    # DO NOT LEAVE THE BELOW FUNCTION IN FINAL PRODUCT
    # Pulled directory from stack overflow
    # def test_djwto(self):

    #     print("---")
    #     print("---")
    #     print("---")
    #     print("test1 running")

    #     url = reverse("user_token")
    #     # url = reverse('api-jwt-auth')
    #     u = User.objects.create_user(
    #         username="user", email="user@foo.com", password="pass"
    #     )
    #     u.is_active = False
    #     u.save()

    #     resp = self.client.post(
    #         url, {"email": "user@foo.com", "password": "pass"}, format="json"
    #     )
    #     self.assertEqual(resp.status_code, 403)
    #     # self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    #     # resp.set_cookie
    #     u.is_active = True
    #     u.save()

    #     login_url = reverse("login")
    #     print("Log in url: ", login_url)
    #     request = self.client.post(
    #         login_url, {"username": "user", "password": "pass"},
    #           format="json"
    #     )
    #     # response = json.loads(request)
    #     print("Access Token: ", request)  # .COOKIES['jwt_access_token'])

    # test = Form()
    # test.append("username")

    # const form = new FormData();
    # form.append("username", username);
    # form.append("password", password);
    # const response = await fetch(url, {
    # method: "post",
    # credentials: "include",
    # body: form,
    # });

    # resp = self.client.post(url, {'username':'user@foo.com',
    # 'password':'pass'}, format='json')
    # self.assertEqual(resp.status_code, 200)
    # self.assertTrue('token' in resp.data)
    # token = resp.data['token']
    # print(token)

    # how we can set a token manually:
    # client.cookies[key] = data

    # verification_url = reverse('api-jwt-verify')
    # resp = self.client.post(verification_url,
    #  {'token': token}, format='json')
    # self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # resp = self.client.post(verification_url, {'token': 'abc'},
    #  format='json')
    # self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # client = APIClient()
    # client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
    # resp = client.get('/api/v1/account/', data={'format': 'json'})
    # self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
    # client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    # resp = client.get('/api/v1/account/', data={'format': 'json'})
    # self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # print("---")
    # print("---")
    # print("---")

    def test_list_users(self):
        response = self.client.get("/users/")
        content = response.json()
        self.assertEqual(response.status_code, 200)
        for user in content["users"]:
            if user["username"] == self.user.username:
                self.assertEqual(user["id"], self.user.id)
            elif user["username"] == self.friend.username:
                self.assertEqual(user["id"], self.friend.id)

    def test_create_user(self):
        data = json.dumps(
            {
                "id": 1,
                "username": "TestCreate",
                "password": "testpassword",
                "first_name": "Test",
                "last_name": "Create",
                "email": "thisisatest@gmail.com",
                "profile_description": "this is a test for creatine a user",
                "profile_photo": "",
                "city": "Kalamazoo",
                "state": "MI",
            }
        )
        response = self.client.post(
            "/users/",
            data,
            content_type="application/json",
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["user"]["id"])

    def test_get_user_details(self):
        response = self.client.get("/users/2/")
        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["id"], self.user.id)

    def test_update_friends_and_activity_lists(self):
        data = json.dumps({"favorite_activities": [1], "friends": [3]})
        response = self.client.put(
            "/users/2/",
            data,
            content_type="application/json",
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        for activity in data["favorite_activities"]:
            if activity["name"] == self.activity.name:
                self.assertEqual(activity["name"], self.activity.name)
        for friend in data["friends"]:
            self.assertEqual(friend["username"], self.friend.username)

    def test_list_ActivityVO(self):
        response = self.client.get("/users/activities/")
        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["ActivityVOs"][0]["id"], self.activity.id)
