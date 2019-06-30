from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
class UserCreationForm1(UserCreationForm):
    email = forms.EmailField( required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm1, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    subscriptions = forms.CharField(label='contact',widget=forms.TextInput))
    address = forms.CharField(label='address',widget=forms.TextInput(attrs={'placeholder':'Address','class':'form-control','id':'search-bar'}))
    birth_date = forms.DateField(label='Date',widget=forms.TextInput(attrs={'type': 'date','placeholder':'Date Of Birth','class':'form-control','id':'search-bar'}))
    class Meta:
        model = UserProfile
        fields = ['contact', 'address', 'birth_date']