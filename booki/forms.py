""" forms """
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile, Review
from .utils import geo


User = get_user_model()


class HomeSearchField(forms.Form):
    """Home search field"""
    query = forms.CharField(
        label='',
        max_length=255,
        min_length=4,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search for Book, ISBN, Author, Genre, ... ',
            'class': 'w-100 fs-3 mb-4'
        })
    )


class LoginForm(forms.Form):
    """Login form"""
    username_email = forms.CharField(
        label='Username/E-mail:',
        min_length=3,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username/E-mail',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        min_length=5,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        })
    )

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))


class RegisterForm(UserCreationForm):
    """ Register form """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'password2', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name:'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name:'}),
        }


class UserProfileForm(forms.ModelForm):
    """ User Profile Form """
    pic = forms.ImageField(label='pic', required=False, widget=forms.FileInput(
        attrs={'class': 'visually-hidden'}
    ))

    address = forms.CharField(label='Address', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Address'}
    ))

    zip_code = forms.CharField(label='Zip Code', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Zip Code'}
    ))

    city = forms.CharField(label='City', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'City'}
    ))

    country = forms.CharField(label='Country', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Country'}
    ))

    phone = forms.CharField(label='Phone', max_length=20, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone'}
    ))

    latitude = forms.FloatField(label='', required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(label='', required=False, widget=forms.HiddenInput())

    def check_valid_address(self):
        """Check and fetch longitude and latitude"""
        check_address = ['address', 'zip_code', 'city', 'country']
        if any(value in self.changed_data for value in check_address) or not self.instance.longitude or not self.instance.latitude:
            self.instance.longitude, self.instance.latitude = geo.get_long_lat(
                self.cleaned_data['address'],
                self.cleaned_data['zip_code'],
                self.cleaned_data['city'],
                self.cleaned_data['country']
            )
            return True if self.instance.longitude and self.instance.latitude else False
        return True

    class Meta:
        model = UserProfile
        fields = ('pic', 'address', 'zip_code', 'city', 'country', 'phone', 'latitude', 'longitude')
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rate', 'comment']
