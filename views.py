from django.shortcuts import render, redirect
from .form import RegisterForm
from .models import Registeruser
from django.core.mail import send_mail
from django.conf import settings
from .form import PasswordForm
from .form import LoginForm
from django.contrib import messages
import uuid
from django.views.decorators.cache import cache_control
from .decorator import user_required
import qrcode
import os
from .form import QRForm

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def home(request):
    
    current = None
    if request.method == 'POST':

        forms = RegisterForm(request.POST, request.FILES)

        if forms.is_valid():
            token = uuid.uuid4()
            if Registeruser.objects.filter(email=forms.cleaned_data['email']).exists():
                messages.error(request, "Email already registered")
                return redirect('home')
            
            else:
                current = Registeruser.objects.create(
                    name=forms.cleaned_data['name'],
                    age=forms.cleaned_data['age'],
                    phone_num=forms.cleaned_data['phone_num'],
                    email=forms.cleaned_data['email'],
                    gender=forms.cleaned_data['gender'],
                    dob=forms.cleaned_data['dob'],
                    course = forms.cleaned_data['course'],          
                    interests = forms.cleaned_data['interests'],
                    pfpic=forms.cleaned_data['pfpic'],

                    verification_token=token
                )
                print(current.email)
            
                verification_link = f"http://127.0.0.1:8000/set-password/{token}/"

                try:
                    html_message = f'<p>Please <a href= "http://127.0.0.1:8000/set-password/{token}/">click here</a> to verify your account.</p>'
                    send_mail(
                        subject="Verify Your Account",
                        message=f"""
                        Welcome!

                        Click Here to Set Password
                        {verification_link}
                        """,
                        from_email=settings.EMAIL_HOST_USER, recipient_list=[current.email], html_message = html_message
                        )
                except Exception as e:
                    messages.error(request, "Verification email failed")
                    return redirect('home')
                
                return redirect('profile', id=current.id)

    else:
        forms = RegisterForm()
    
    return render(request, "input.html", {"forms": forms})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def set_password(request, token):
    try:
        user = Registeruser.objects.get(verification_token=token)
    except Registeruser.DoesNotExist:
        messages.error(request, 'This link has already been used')
        return render(request, 'expired.html')

    if request.method == "POST":
        form = PasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm_password']

            if password == confirm:
                user.password = password
                user.is_verified = True
                user.verification_token = None

                user.save()

                return redirect('login')
            else:
                messages.error(request, 'Enter same password in both the field')
    else:
        form = PasswordForm()

    return render(request, "password.html", {'form': form})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = Registeruser.objects.get(email=email)
                if (user.password == password and user.is_verified):
                    request.session['user_id'] = user.id
                    return redirect('selection')
                
            except Registeruser.DoesNotExist:
                messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {'form': form})

@user_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def profile(request, id):
    user = Registeruser.objects.get(id=id)
    return render(request, "profile.html", {"user": user})

@user_required
def qr_generator(request):

    if request.method == "POST":
        form = QRForm(request.POST)
        if form.is_valid():

            text = form.cleaned_data['text']
            filename = f"{uuid.uuid4()}.png"
            folder = os.path.join(settings.MEDIA_ROOT, 'qr')

            if not os.path.exists(folder):
                os.makedirs(folder)

            filepath = os.path.join(folder, filename)

            image = qrcode.make(text)

            image.save(filepath)
            return render(request, 'image.html', {'form': form, 'img': filename})

    else:
        form = QRForm()
    return render(request, 'image.html', {'form': form})

@user_required
def selection(request):
    return render(request, 'selection.html')

@user_required
def url_qr(request):
    if request.method == "POST":
        url = request.POST.get('url')

        filename = f"{uuid.uuid4()}.jpg"
        folder = os.path.join(settings.MEDIA_ROOT, 'qr_codes')

        if not os.path.exists(folder):
            os.makedirs(folder)

        filepath = os.path.join(folder, filename)
        image = qrcode.make(url)
        image.save(filepath)

        return render(request, 'urlqr.html',{'img': filename})

    return render(request, 'urlqr.html')