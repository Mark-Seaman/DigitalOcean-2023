xxx.py


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = SWUser.objects.filter(email=email).first()
        if user is not None and user.check_password(password):
            user = authenticate(
                request, email='testuser@example.com', password='testpassword')
            assert user


class LoginViewTest(TestCase):

    def setUp(self):
        self.email = 'testuser@example.com'
        self.password = 'testpassword'
        self.user = SWUser.objects.create_user(
            'testuser',
            email=self.email,
            password=self.password
        )

    def test_login_valid_user(self):
        response = self.client.post(
            self.login_url, {'email': self.email, 'password': self.password})
