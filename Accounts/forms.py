
from django import forms
from .models import User
from utils.check_valid.check_information import Check_Email,check_username ,check_phone
# from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UsercreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput,required=False)
    password2 = forms.CharField(widget=forms.PasswordInput,required=False)

    class Meta:
        model = User
        fields = ('email','username','phone')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError('password not math')
        if len(password2) < 7:
            raise forms.ValidationError('password not 8 ')

        return password1
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError('email airly exist')
        if Check_Email(email):
            return email
        raise forms.ValidationError('email airly exist')
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise forms.ValidationError('username airly exist')
        if check_username(username):
            return username
        raise forms.ValidationError('username airly exist')
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone=phone).exists()
        if user==False:
            if check_phone(phone):
                return phone
        raise forms.ValidationError('phone airly exist','ss')
        
    
    def save(self, commit= False):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    



# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = []


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

# class UserRegisterForm(forms.Form):
#     username = forms.CharField(max_length=50)
#     email = forms.EmailField(max_length=50)

#     phone = forms.CharField(max_length=13)
#     password1 = forms.CharField(max_length=200)
#     password2 = forms.CharField(max_length=200)

    