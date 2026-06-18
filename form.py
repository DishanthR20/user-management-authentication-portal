from django import forms
from phonenumber_field.formfields import PhoneNumberField

class RegisterForm(forms.Form):

    name = forms.CharField(label = "Name ")
    age = forms.IntegerField(label = "Age ")
    phone_num = PhoneNumberField()
    email = forms.EmailField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = forms.ChoiceField(choices = GENDER_CHOICES, label="Gender") 
    dob = forms.DateField(label="Date of Birth")
    pfpic = forms.ImageField()

    INTEREST_CHOICES = [
        ('tech', 'Technology'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('read', 'Reading'),
        ('sleep', 'Sleeping'),
    ]

    interests = forms.MultipleChoiceField(choices=INTEREST_CHOICES, widget=forms.CheckboxSelectMultiple(), label="Select your Interests")

    COURSE_CHOICES = [
        ('cse', 'CSE'),
        ('ece', 'ECE'),
        ('other', 'Other'),
    ]

    course = forms.ChoiceField(choices=COURSE_CHOICES, widget=forms.RadioSelect(), label="Select your Course")

class PasswordForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput()) 

class UpdateForm(forms.Form):
    name = forms.CharField(label="Name")
    age = forms.IntegerField(label="Age")
    phone_num = PhoneNumberField()
    email = forms.EmailField()

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label="Gender"
    )

    dob = forms.DateField(label="Date of Birth")

    COURSE_CHOICES = [
        ('cse', 'CSE'),
        ('ece', 'ECE'),
        ('other', 'Other'),
    ]

    course = forms.ChoiceField(
        choices=COURSE_CHOICES,
        widget=forms.RadioSelect()
    )

    INTEREST_CHOICES = [
        ('tech', 'Technology'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('read', 'Reading'),
        ('sleep', 'Sleeping'),
    ]

    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple()
    )

    pfpic = forms.ImageField(required=False)

class QRForm(forms.Form):
    text = forms.CharField(label="Enter Text", widget=forms.Textarea(attrs={'rows': 4,'placeholder': 'Enter text for QR Code'}))