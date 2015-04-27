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

	# If user enter wrong data
	def set_initial(self, username):
		self.fields['username'].initial = username


class SignUpForm(forms.Form):

	# Regular expressions:	first symbol is letter
	username = forms.RegexField(initial='', regex=r'^\D+[0-9a-zA-Z]+$', label='Username', max_length=50, 
		widget=forms.TextInput (attrs={
			'class': 'form-control',
			'placeholder': 'Be unique',
			}))
	email = forms.EmailField(initial='', label='Email', max_length=100, 
		widget=forms.EmailInput(attrs={
			'class': 'form-control',
			'placeholder': 'Keep in touch'
			}))
	password = forms.CharField(label='Password', max_length=50, 
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


class AskForm(forms.Form):
	title = forms.CharField(initial='', label='Title', max_length=100, 
		widget=forms.TextInput (attrs={
			'class': 'form-control',
			'placeholder': 'Briefly about the question',
			}))
	text = forms.CharField(label='Text',  
		widget=forms.Textarea(attrs={
			'class': 'form-control',
			'placeholder': 'Details here',
			'rows':'5'
			}))
	tags = forms.CharField(initial='', label='Tags', max_length=50, required=False, 
	widget=forms.TextInput (attrs={
		'class': 'form-control',
		'placeholder': 'Quickly find',
		}))


class AnswerForm(forms.Form):
	text = forms.CharField(label='',  
		widget=forms.Textarea(attrs={
			'class': 'form-control',
			'placeholder': 'Enter your answer',
			'rows':'3'
			}))
	

class EditProfileForm(forms.Form):
	first_name = forms.CharField(initial='', label='First name', max_length=100, 
		widget=forms.TextInput (attrs={
			'class': 'form-control',
			'placeholder': '',
			}))
	last_name = forms.CharField(initial='', label='Last name', max_length=100, required=False,
		widget=forms.TextInput (attrs={
			'class': 'form-control',
			'placeholder': '',
			}))


class EditPhotoForm(forms.Form):
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


class ChangePasswordForm(forms.Form):
	password = forms.CharField(label='Password', max_length=100, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': '12345'
			}))
	new_password = forms.CharField(label='New password', max_length=100, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': '54321'
			}))
	repeat_new_password = forms.CharField(label='Repeat new password', max_length=100, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': '54321'
			}))

