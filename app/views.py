#importing all required libraries and modules
from django.conf import settings
import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.db.models import Sum, Q
from datetime import datetime
import json
from .forms import ExpenseForm, ExpensePaymentForm
from .models import ExpensePayment

#home function /dashboard
@login_required
def HomeView(request):
    return render(request, 'home.html')

#sign up page
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')  
    else:
        form = UserCreationForm()  

    return render(request, 'signup.html', {'form': form})  



#login page      
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on user role
            if user.is_superuser:
                print("Redirecting to admin panel")
                return redirect(reverse('admin:index'))
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

#logout function
def logout_view(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('login')

