from django import forms
import os
from django.core.files import File
from django.core.validators import ValidationError


class LoginForm(forms.Form):
	username = forms.CharField(initial='', label='Username', max_length=100, 
		widget=forms.TextInput (attrs={
			'class': 'form-control',
			'placeholder': 'Unique',
			}))
	password = forms.CharField(label='Password', max_length=100, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': '12345'
			}))

	#	If user enter wrong data
	def set_initial(self, username):
		self.fields['username'].initial = username


class SignUpForm(forms.Form):
	username = forms.CharField(initial='', label='Username', max_length=100, 
		widget=forms.TextInput (attrs={
			'class': 'form-control',
			'placeholder': 'Be unique',
			}))
	email = forms.EmailField(initial='', label='Email', max_length=100, 
		widget=forms.EmailInput(attrs={
			'class': 'form-control',
			'placeholder': 'Keep in touch'
			}))
	password = forms.CharField(label='Password', max_length=100, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': '12345'
			}))
	pic = forms.ImageField(label='File input', required=False)

	def check_pic(self):
		max_size = 4
		pic = self.cleaned_data.get('pic',False)
		if pic:
			if pic._size > max_size * 1024 * 1024:
				print '#1'
				raise ValidationError("large size")
				print '#2'
			return pic
		else:
			raise ValidationError("Couldn't read uploaded image")



def handleUploadedFile(f):
	filename = os.path.dirname(os.path.dirname(__file__)) + '/uploads/' + f.name
	with open(filename, 'wb') as destination:
		destination.write(f.read())
	return f.name