from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model


UserModel = get_user_model()

class RegisterUserForm(auth_forms.UserCreationForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["password"].widget.attrs["placeholder"] = "Password"

    class Meta:
        model = UserModel
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Password"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Repeat password"}),

        }
        error_messages = {
            "email": {"invalid": "Please enter a valid email like john@email.com"},
        }


class LoginUserForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["password"].widget.attrs["placeholder"] = "Password"
