import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserChangeForm
# from django.contrib.auth.models import User This changed to catalog.MyUser
from catalog.models import MyUser
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
	email = forms.EmailField(label=False, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'Email Address', 'autocomplete': 'off'}))
	password = forms.CharField(label=False, required=True, help_text=None, widget=forms.PasswordInput(attrs={'placeholder': 'Input password', 'autocomplete': 'off'}))

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		if email and password:
			user = authenticate(username = email, password = password)
			if not user:
				raise ValidationError("User doesn't exist.")
			if not user.check_password(password):
				raise ValidationError("Incorrect Password")
			if not user.is_active:
				raise ValidationError("User is not active.")

		return super(LoginForm, self).clean(*args, **kwargs)

class SignUpForm(forms.ModelForm):
	first_name = forms.CharField(label=False, max_length=50, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'autocomplete': 'off'}))
	last_name = forms.CharField(label=False, max_length=50, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'autocomplete': 'off'}))
	email = forms.EmailField(label=False, max_length=254, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'Email address', 'autocomplete': 'off'}))
	date_of_birth = forms.DateField(label=False, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'Date of Birth : YYYY-MM-DD'}))
	password1 = forms.CharField(label=False, required=True, help_text=None, widget=forms.PasswordInput(attrs={'placeholder': 'Input password', 'autocomplete': 'off'}))
	password2 = forms.CharField(label=False, required=True, help_text=None, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'autocomplete': 'off'}))

	class Meta:
		model = MyUser
		# If you want the username field to be there - uncomment it up there and pass its location in the fields below
		fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2']
	def clean_password2(self):
		# Check if the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(SignUpForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class ResetPasswordForm(PasswordResetForm):
	email = forms.EmailField(label=False, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'Email Address', 'autocomplete': 'off'}))

	# def clean(self, *args, **kwargs):
	# 	email = self.cleaned_data.get('email')
	# 	return super(PasswordResetForm, self).clean(*args, **kwargs)
	class Meta:
		model=MyUser
		fields = ('email')

class PasswordSetForm(SetPasswordForm):
	new_password1 = forms.CharField(label=False, required=True, help_text=None, widget=forms.PasswordInput(attrs={'placeholder': 'Input password', 'autocomplete': 'off'}))
	new_password2 = forms.CharField(label=False, required=True, help_text=None, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'autocomplete': 'off'}))

	class Meta:
		model=MyUser
		fields=('new_password1', 'password2')

class EditProfileForm(forms.Form):
	first_name = forms.CharField(label=False, max_length=50, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'autocomplete': 'off'}))
	last_name = forms.CharField(label=False, max_length=50, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'autocomplete': 'off'}))
	email = forms.EmailField(label=False, max_length=254, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'Email address', 'autocomplete': 'off'}))
	date_of_birth = forms.DateField(label=False, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'Date of Birth : YYYY-MM-DD'}))

	class Meta:
		model = MyUser
		fields = ('first_name', 'last_name', 'email', 'date_of_birth')


class ContactForm(forms.Form):
	name = forms.CharField(label='Your Name', max_length=100, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'Enter your name', 'autocomplete': 'off'}))
	email = forms.EmailField(label='Email', max_length=254, required=True, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'Enter your email address', 'autocomplete': 'off'}))
	message = forms.CharField(label='Message', max_length=1000, required=True, help_text=None, widget=forms.Textarea(attrs={'placeholder': 'Enter your message', 'autocomplete': 'on'}))


class RenewBookForm(forms.Form):
	renewal_date = forms.DateField(label='New Date', help_text=None, widget=forms.TextInput(attrs={'placehodler': 'Enter a new book available date'}))

	def clean_renewal_date(self):
		data = self.cleaned_data['renewal_date']

		# Check if the date is not in the past
		if data < datetime.date.today():
			raise ValidationError(_('Renewal in the past'))

		# Check if the date is in allowed range(+4weeks from today)
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('Renewal more than 4 weeks ahead.'))

		# Return the cleaned data
		return data