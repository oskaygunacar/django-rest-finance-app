from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse

#forms
from account.forms import userSignupForm, LoginForm, ChangePasswordForm

# signup view

def signup_view(request):
    form = userSignupForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password) # hashing the password - user.set_password(password) ile kullanıcıdan gelen password'u hashliyoruz. Bu veritabanına kayıt ederken daha güvenli olmasını sağlar + gereklidir.
        user_obj = user.save()
        messages.success(request, 'Account created successfully')
        return redirect('account:login')
    return render(request, 'account/login_signup.html', {'form': form, 'title': 'Signup'})


#login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.META.get('HTTP_REFERER')) if request.META.get('HTTP_REFERER') else redirect('/')
        else:
            messages.info(request, 'Username or password is incorrect! Please check and try again.')
            return redirect('account:login')
    return render(request, 'account/login_signup.html', {'form': form, 'title': 'Login'})

#logout
@login_required(login_url='account:login')
def logout_view(request):
    if request.user.is_authenticated and request.method == 'GET':
        logout(request)
        return redirect('/')
    return redirect(request.META.get('HTTP_REFERER')) if request.META.get('HTTP_REFERER') else redirect('/') # if user is not authenticated, redirect to the user's previous page. If there is no previous page, redirect to the home page.

#change password
@login_required(login_url='account:login')
def change_password_view(request):
    if request.method == 'GET':
        form = ChangePasswordForm(request.POST or None)
        if form.is_valid():
            user = get_object_or_404(User, id=request.user.id)
            old_password = form.cleaned_data.get('old_password')
            if not user.check_password(old_password):
                messages.error(request, 'Old password is incorrect')
                return redirect('account:change_password')
            if user.check_password(form.cleaned_data.get('new_password')):
                messages.error(request, 'New password cannot be the same as the old password')
                return redirect('account:change_password') 
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            logout(request)
            messages.success(request, 'Password changed successfully')
            return redirect('account:login')
        return render(request, 'account/login_signup.html', {'form': form, 'title': 'Change Password'})

@login_required(login_url='account:login')
def user_api_token(request):
    if request.method == 'GET':
        token = Token.objects.get(user=request.user)
        return render(request, 'account/apiToken.html', {'token': token.key})

@login_required(login_url='account:login')
def user_api_new_token_generate_view(request):
    if request.method == 'GET':
        token = Token.objects.get(user=request.user)
        token.delete()
        Token.objects.create(user=request.user)
        token = Token.objects.get(user=request.user)
        return JsonResponse({'status': 200, 'message': 'New token generated successfully', 'token':token.key})