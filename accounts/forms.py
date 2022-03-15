from django import forms
from django.contrib.auth import password_validation, authenticate
from django.db.transaction import commit
from django.shortcuts import redirect
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, SetPasswordForm
from django.core.exceptions import ObjectDoesNotExist
import hashlib


class LoginForm(AuthenticationForm):
    answer = forms.IntegerField(help_text='3+3 = ?')

    def clean_answer(self):
        answer = self.cleaned_data.get('answer')
        if answer != 6:
            raise forms.ValidationError('정답이아닙니다.')
        return answer


class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'name', 'institution', 'department', 'employee_no', 'mobile_phone', 'company_phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'requried': True,
            'class' : "input",
            'size': '10',
        })
        self.fields['password1'].widget.attrs.update({
            'requried': True,
            'class' : "input",
            'size': '10',
        })
        self.fields['password2'].widget.attrs.update({
            'requried': True,
            'class' : "input",
            'size': '10',
        })
        self.fields['name'].widget.attrs.update({
            'requried': True,
            'class' : "input",
            'size': '10',
        })
        self.fields['email'].widget.attrs.update({
            'requried' : True,
            'class': "input",
            'size': '10',
        })
        self.fields['institution'].widget.attrs.update({
            'class': "input",
            'size': '10',
        })
        self.fields['department'].widget.attrs.update({
            'class': "input",
            'size': '10',
        })
        self.fields['employee_no'].widget.attrs.update({
            'class': "input",
            'size': '10',
        })
        self.fields['mobile_phone'].widget.attrs.update({
            'class': "input",
            'size': '10',
        })
        self.fields['company_phone'].widget.attrs.update({
            'class': "input",
            'size': '10',
        })
        #self.fields['username'].label = 'Id'
        #self.fields['username'].help_text = None

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if len(username) < 4:
                raise forms.ValidationError("Please enter at least 4 characters.")
            qs = User.objects.filter(username=username)
            if qs.exists():
                raise forms.ValidationError("ID is already registered.")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError("Please enter at least 6 characters.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if len(password2) < 6:
            raise forms.ValidationError("Please enter at least 6 characters.")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The two password fields didn’t match.')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("This E-mail is already registered.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}), label="Id")
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': "off"}),
    )

    def confirm_login_allowed(self, user):
        if not user.state == 'liv':
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password."
        ),
        'inactive': ("This account is unapproved."),
    }


class RecoveryIdForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']

    def clean_email(self):
        name = self.cleaned_data.get("name")
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(name=name, email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError("The information you entered does not match or does not exist.")
        return email


class RecoveryPwForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email']


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError("Please enter at least 6 characters.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if len(password2) < 6:
            raise forms.ValidationError("Please enter at least 6 characters.")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The two password fields didn’t match.')
        return password2


