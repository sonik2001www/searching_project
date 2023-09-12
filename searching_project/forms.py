from django import forms
from allauth.account.forms import SignupForm
from allauth.account.models import EmailAddress


class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="Name")
    # age = forms.IntegerField(label='Вік')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and EmailAddress.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def save(self, request):
        first_name = self.cleaned_data.get('first_name')
        # age = self.cleaned_data.get('age')

        user = super(MyCustomSignupForm, self).save(request)
        print(user)
        if user:
            user.first_name = first_name
            # user.age = age
            user.save()

        return user

