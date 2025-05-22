# models.py
from django.db import models
from django.contrib.auth.models import User

class ExpensePayment(models.Model):
    CATEGORY_CHOICES = [
        ("Food", "Food"),
        ("Travel", "Travel"),
        ("Bills", "Bills"),
        ("Shopping", "Shopping"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default="Created")  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount} - {self.status}"
