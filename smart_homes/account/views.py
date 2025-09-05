from django.contrib.auth import views as auth_views, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as generic_views
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from smart_homes.account.forms import LoginUserForm, RegisterUserForm


UserModel = get_user_model()

class RegisterUserView(generic_views.CreateView):
    template_name = "account/register.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, form.instance)
        messages.success(self.request, "Registration successful. Welcome!")
        return response


class LoginUserView(auth_views.LoginView):
    template_name = "account/login.html"
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy("home")


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "You were successfully logged out.")
    return redirect("home")


class ProfileUserView(LoginRequiredMixin, generic_views.DetailView):
    model = UserModel
    template_name = "account/profile.html"
    context_object_name = "user_object"

    def get_object(self, queryset=None):
        return self.request.user
