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


#fetching razor pay test credentials from setting
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#login_required is passed so only this page will open when the user is authenticated
@login_required
def create_expense_payment(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            amount_paise = int(expense.amount * 100)

            # Razorpay order creation
            order = razorpay_client.order.create({
                "amount": amount_paise,
                "currency": "INR",
                "payment_capture": "1"
            })
            expense.order_id = order["id"]
            expense.save()
            context = {
                "form": form,
                "order": order,
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "expense": expense
            }
            return render(request, "checkout.html", context)
    else:
        form = ExpenseForm()
    return render(request, "expense_form.html", {"form": form})

#this is the success page after successful payment
@csrf_exempt
@login_required
def payment_success(request):
    if request.method == "POST":
        order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        signature = request.POST.get("razorpay_signature")
        params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        }
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            status = "Completed"
        except:
            status = "Failed"
        payment = ExpensePayment.objects.filter(order_id=order_id).first()
        if payment:
            payment.payment_id = payment_id
            payment.status = status
            payment.save()
            if status == "Completed":
                return render(request, "payment_success.html", {"payment": payment})
        return render(request, "payment_failed.html", {"error": "Payment failed."})
    return redirect("create_expense_payment")

@login_required
def payment_success_page(request):
    payment_id = request.GET.get('payment_id')
    payment = None
    if payment_id:
        from .models import ExpensePayment
        payment = ExpensePayment.objects.filter(payment_id=payment_id, user=request.user, status="Completed").first()
    return render(request, "payment_success.html", {"payment": payment})

#payment failed page
@login_required
def payment_failed_page(request):
    error_msg = request.GET.get('error', None)
    return render(request, "payment_failed.html", {"error": error_msg})

