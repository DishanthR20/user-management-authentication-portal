from django.shortcuts import render, redirect
from myapp.models import Registeruser
from myapp.form import RegisterForm
from myapp.form import UpdateForm
from django.contrib import messages
from .decorators import admin_required
from .models import AdminUser
from .forms import AdminRegisterForm, AdminLoginForm
from django.views.decorators.cache import cache_control
from django.conf import settings
import uuid
import os
from django.http import JsonResponse
import qrcode

@admin_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def user_list(request):
    users = Registeruser.objects.all()
    return render(request, 'custom_admin/user_list.html', {'users': users})

@admin_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def delete_user(request, id):
    user = Registeruser.objects.get(id=id)
    user.delete()
    return redirect('user_list')

@admin_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def add_user(request):

    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            if Registeruser.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, "Email already registered")
                return redirect('add_user')
            else:
                Registeruser.objects.create(
                    name=form.cleaned_data['name'],
                    age=form.cleaned_data['age'],
                    phone_num=form.cleaned_data['phone_num'],
                    email=form.cleaned_data['email'],
                    gender=form.cleaned_data['gender'],
                    dob=form.cleaned_data['dob'],
                    course=form.cleaned_data['course'],
                    interests=form.cleaned_data['interests'],
                    pfpic=form.cleaned_data['pfpic'],
                    is_verified=True
                )

                return redirect('user_list')

    else:
        form = RegisterForm()

    return render(request, 'custom_admin/add_user.html', {'form': form})

@admin_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def update_user(request, id):
    user = Registeruser.objects.get(id=id)

    if request.method == "POST":
        form = UpdateForm(request.POST, request.FILES)

        if form.is_valid():
            user.name = form.cleaned_data['name']
            user.age = form.cleaned_data['age']
            user.phone_num = form.cleaned_data['phone_num']
            user.email = form.cleaned_data['email']
            user.gender = form.cleaned_data['gender']
            user.dob = form.cleaned_data['dob']
            user.course = form.cleaned_data['course']
            user.interests = form.cleaned_data['interests']

            if form.cleaned_data['pfpic']:
                user.pfpic = form.cleaned_data['pfpic']

            user.save()

            return redirect('user_list')
        
    else:
        form = UpdateForm(initial={
            'name': user.name,
            'age': user.age,
            'phone_num': user.phone_num,
            'email': user.email,
            'gender': user.gender,
            'dob': user.dob,
            'course': user.course,
            'interests': user.interests,
        })

    return render(request, 'custom_admin/update_user.html', {'form': form})

@admin_required
def user_qr(request, id):

    users = Registeruser.objects.all()
    user_details = Registeruser.objects.get(id=id)
    data = f"""
            Name: {user_details.name}
            Age: {user_details.age}
            """

    filename = f"{uuid.uuid4()}.png"
    folder = os.path.join(settings.MEDIA_ROOT, 'qr')

    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, filename)
    image = qrcode.make(data)

    image.save(filepath)
    return render(request, 'custom_admin/user_list.html', {'users': users, 'img': filename})


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def create_admin(request):

    if request.method == "POST":

        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if AdminUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")

            elif AdminUser.objects.filter(email=email).exists():
                messages.error(request, "Mail already exists")

            else:
                AdminUser.objects.create(username=username, email=email, password=form.cleaned_data['password'])

                messages.success(request,"Admin created successfully")


    else:
        form = AdminRegisterForm()

    return render(request, 'custom_admin/create_admin.html', {'form': form})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def admin_login(request):
    
    if request.session.get('admin_id'):
        return redirect('user_list')
    
    if request.method == "POST":

        form = AdminLoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                admin = AdminUser.objects.get(username=username)
                if admin.password == password:
                    request.session['admin_id'] = admin.id
                    return redirect('user_list')
                
                else:
                    messages.error(request, "Invalid password")

            except AdminUser.DoesNotExist:
                messages.error(request, "Admin not found")
    else:
        form = AdminLoginForm()

    return render(request, 'custom_admin/admin_login.html', {'form': form})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')