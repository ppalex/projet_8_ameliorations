from django.test import TestCase
from users.forms import (CustomUserCreationForm, ProfileUpdateForm,
                         UserUpdateForm)


class CustomUserCreationFormTest(TestCase):
    def test_form(self):

        data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'Alsjdsd52&',
            'password2': 'Alsjdsd52&',
        }

        form = CustomUserCreationForm(data)

        self.assertTrue(form.is_valid())

    def test_clean_username(self):
        data = {
            'username': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password1': 'Alsjdsd52&',
            'password2': 'Alsjdsd52&',
        }

        form = CustomUserCreationForm(data)
        if form.is_valid():
            username = form.cleaned_data.get("username")

        self.assertEqual(username, 'testuser1')

    def test_clean_email(self):
        data = {
            'username': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password1': 'Alsjdsd52&',
            'password2': 'Alsjdsd52&',
        }

        form = CustomUserCreationForm(data)
        if form.is_valid():
            email = form.cleaned_data.get("email")

        self.assertEqual(email, 'testuser1@gmail.com')


class UserUpdateFormTest(TestCase):
    def test_form(self):

        data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',

        }

        form = UserUpdateForm(data)

        self.assertTrue(form.is_valid())


class ProfileUpdateFormTest(TestCase):
    def test_form(self):

        data = {
            'image': 'testuser',
           
        }

        form = ProfileUpdateForm(data)

        self.assertTrue(form.is_valid())
