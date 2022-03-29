from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	phoneno = forms.IntegerField(required=True)

	class Meta:
		model = User
		fields = ("username", "phoneno", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.number = self.cleaned_data['number']
		if commit:
			user.save()
		return user
