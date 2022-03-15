from django import forms
from django.contrib.auth import password_validation
from django.shortcuts import redirect
from accounts.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField


class UserModifyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'mobile_phone', 'institution', 'department', 'employee_no', 'company_phone', 'state', 'role', 'level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'readonly': True,
            'requried': True,
            'class' : "input",
            'id' : '',
        })
        # self.fields['password'].widget.attrs.update({
        #     'type': 'password',
        #     'requried': True,
        #     'class' : "input",
        #     'id' : 'input_password',
        # })
        self.fields['name'].widget.attrs.update({
            'requried': True,
            'class' : "input",
            'id' : '',
        })
        self.fields['email'].widget.attrs.update({
            'requried' : True,
            'class': "input",
            'id': '',
        })
        self.fields['department'].widget.attrs.update({
            'requried' : True,
            'class': "input",
            'id': '',
        })
        self.fields['employee_no'].widget.attrs.update({
            'requried' : True,
            'class': "input",
            'id': '',
        })
        self.fields['mobile_phone'].widget.attrs.update({
            'requried' : True,
            'class': "input",
            'id': '',
        })
        self.fields['company_phone'].widget.attrs.update({
            'requried' : True,
            'class': "input",
            'id': '',
        })
        self.fields['state'].widget.attrs.update({
            'requried' : True,
            'class': "",
            'id': '',
        })
        self.fields['role'].widget.attrs.update({
            'requried' : True,
            'class': "",
            'id': '',
        })
        self.fields['level'].widget.attrs.update({
            'requried' : True,
            'class': "",
            'id': '',
        })

    #def clean_password(self):
        #password = self.cleaned_data.get("password")
        #if len(password) < 6:
            #raise forms.ValidationError("Please enter at least 6 characters.")
        #return password

    #def clean_email(self):
        #email = self.cleaned_data.get('email')
        #if email:
            #qs = User.objects.filter(email=email)
            #if qs.exists():
                #raise forms.ValidationError("email is already registered.")
        #return email
