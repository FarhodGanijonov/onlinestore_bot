from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product

User = get_user_model()

class Order(models.Model):
    user_id = models.BigIntegerField()  # Telegram foydalanuvchi ID
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} | User: {self.user_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # saqlash vaqtidagi narx

    def __str__(self):
        return f"{self.product.name_uz} ({self.quantity}x)"
