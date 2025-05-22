from django import forms
from .models import ExpensePayment

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpensePayment
        fields = ["amount", "description", "date", "category"]
        widgets = {
            "amount": forms.NumberInput(attrs={
                "class": "form-control", 
                "placeholder": "Enter amount"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control", 
                "rows": 3,
                "placeholder": "Describe the transaction"
            }),
            "date": forms.DateInput(attrs={
                "type": "date", 
                "class": "form-control"
            }),
            "category": forms.Select(attrs={
                "class": "form-select"
            }),
        }


class ExpensePaymentForm(forms.ModelForm):
    class Meta:
        model = ExpensePayment
        fields = [
            'amount', 'description', 'date', 'category',
            'order_id', 'payment_id', 'status'
        ]
        widgets = {
            "amount": forms.NumberInput(attrs={
                "class": "form-control", 
                "placeholder": "Enter amount"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control", 
                "rows": 3,
                "placeholder": "Describe the transaction"
            }),
            "date": forms.DateInput(attrs={
                "type": "date", 
                "class": "form-control"
            }),
            "category": forms.Select(attrs={
                "class": "form-select"
            }),
            "order_id": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "Order ID"
            }),
            "payment_id": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "Payment ID"
            }),
            "status": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "Status (e.g. Created, Paid)"
            }),
        }
