from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ShippingAddress, Profile, Contact, Review


class ReviewForm(forms.ModelForm):
  class Meta:
    model = Review
    fields = ['star', 'content']


class ContactForm(forms.ModelForm):
  class Meta:
    model = Contact
    fields = '__all__'


class UpdateUserForm(forms.ModelForm):
  first_name = forms.CharField(label='Họ', widget=forms.TextInput(attrs={'class': 'input-account'}))
  last_name = forms.CharField(label='Tên', widget=forms.TextInput(attrs={'class': 'input-account'}))
  email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'input-account'}))
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email']
    

class UpdateProfileForm(forms.ModelForm):
  phone = forms.CharField(label='Điện thoại', widget=forms.TextInput(attrs={'class': 'input-account'}))
  dob = forms.DateField(label='Ngày sinh', widget=forms.DateInput(attrs={'class': 'input-account', 'type': 'date'}))
  class Meta:
    model = Profile
    fields = ['phone', 'dob']


class ShippingAddressForm(forms.ModelForm):
  class Meta:
    model = ShippingAddress
    exclude = ('user',)
    widgets = {'shipping_full_name': forms.TextInput(attrs={'class': 'input-account'}),
               'shipping_phone': forms.TextInput(attrs={'class': 'input-account'}),
               'shipping_address': forms.TextInput(attrs={'class': 'input-account'}),
               'shipping_city': forms.TextInput(attrs={'class': 'input-account'}),
               'shipping_state': forms.TextInput(attrs={'class': 'input-account'}),}
    labels = {'shipping_full_name': 'Họ tên', 
              'shipping_phone': 'Số điện thoại', 
              'shipping_address': 'Địa chỉ', 
              'shipping_city': 'Thành phố',
              'shipping_state': 'Tỉnh'}


class LoginForm(AuthenticationForm):
  username = forms.CharField(min_length=6, widget=forms.TextInput(attrs={'class': 'input-account'}), label='Tài khoản')
  password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'input-account'}), label='Mật khẩu')
  error_messages = {'invalid_login': "Tên đăng nhập hoặc mật khẩu không đúng."}
  

class RegisterForm(UserCreationForm):
  error_messages = {'invalid': "Người dùng đã tồn tại"}
  class Meta:
    model = User 
    fields = ('username', 'password1', 'password2')
    widgets = {'username': forms.TextInput(attrs={'minlength': 6, 'class': 'input-account'})}
    labels = {'username': 'Tên đăng nhập'}
    help_texts = {'username': ''}
    error_messages = {'username': {'unique': 'Tên đăng nhập này đã tồn tại.'}}

  def __init__(self, *args, **kwargs):
    super(RegisterForm, self).__init__(*args, **kwargs)
    self.fields['password1'].widget.attrs['minlength'] = 8
    self.fields['password1'].widget.attrs['class'] = 'input-account'
    self.fields['password1'].label = 'Mật khẩu'
    self.fields['password1'].help_text = ''
    self.fields['password2'].widget.attrs['minlength'] = 8
    self.fields['password2'].widget.attrs['class'] = 'input-account'
    self.fields['password2'].label = 'Nhập lại mật khẩu'
    self.fields['password2'].help_text = ''