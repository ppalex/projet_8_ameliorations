from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import CustomUserCreationForm

from django.contrib.auth import logout


class RegisterView(View):
    """This class displays the register view.
    """

    register_form = CustomUserCreationForm
    template_name = 'users/register.html'

    def get(self, request):
        form = self.register_form()
        context = {'form': form}

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.register_form(request.POST)
        context = {'form': form}

        if form.is_valid():

            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            authenticate(username=username, password=password)
            messages.success(request, "Votre compte a été créé")

            return redirect('index')

        return render(request, self.template_name, context)


class CustomLoginView(SuccessMessageMixin, LoginView):
    """This class displays the login view.
    """
    success_url = '/'
    success_message = "Vous êtes connectés %(username)s"


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    """This class is used to logout the user.
    """
    success_url = '/'
    success_message = "Vous êtes déconnectés"


class ProfileView(View):
    """This class displays the profile view.
    """
    template_name = 'users/profile.html'

    def get(self, request):
        return render(request, self.template_name)


def custom_logout(request):
    # message user or whatever
    logout(request)
    messages.success(request, "Vous avez été déconnecté")

    return redirect('home')
