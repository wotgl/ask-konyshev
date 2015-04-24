from django import forms
import os

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
	pic = forms.FileField(label='File input', required=False)

	def clean_pic(self):
		print self.fields['pic']



def handleUploadedFile(f):
	filename = os.path.dirname(os.path.dirname(__file__)) + '/uploads/' + f.name
	with open(filename, 'wb') as destination:
		destination.write(f.read())
	return f.name