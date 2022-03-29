from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	number = forms.IntegerField(required=True)

	class Meta:
		model = User
		fields = ("userid", "phoneno", "password", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.number = self.cleaned_data['number']
		if commit:
			user.save()
		return user
