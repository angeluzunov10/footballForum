from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models.app_profile import Profile

UserModel = get_user_model()


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ['email', 'password1', 'password2']

    def clean_email(self):      # validating uniqueness of the email
        email = self.cleaned_data.get('email')
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use!")
        return email


class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
    )

    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'profile_picture': 'Profile picture URL:'
        }

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', UserModel)  # dynamically get the user instance
        super().__init__(*args, **kwargs)

        if user_instance:
            self.fields['username'].initial = user_instance.username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_instance = self.initial.get('user_instance')  # get the current user instance from the form's initial data

        if UserModel.objects.filter(username=username).exclude(pk=user_instance.pk).exists():   # checks if the username already exists in the database, excluding the current user
            raise forms.ValidationError("This username is already taken. Please choose another.")

        return username

    def save(self, commit=True):
        profile = super().save(commit=False)

        user_instance = self.initial.get('user_instance')   # saving changes to the associated UserModel
        if user_instance:
            user_instance.username = self.cleaned_data['username']
            if commit:
                user_instance.save()  # saving changes to the user

        if commit:
            profile.save()  # saving changes to the profile

        return profile


class DeleteProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'favorite_team', 'location']  # Include fields to display

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True
