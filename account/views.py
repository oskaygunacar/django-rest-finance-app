from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

#forms
from account.forms import userForm

# signup view

def signup_view(request):
    form = userForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password) # hashing the password - user.set_password(password) ile kullanıcıdan gelen password'u hashliyoruz. Bu veritabanına kayıt ederken daha güvenli olmasını sağlar + gereklidir.
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('/')
    return render(request, 'account/login_signup.html', {'form': form})