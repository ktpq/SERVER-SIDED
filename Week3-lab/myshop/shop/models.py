from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=150, null=False)

class Customer(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=150, null=False)
    address = models.JSONField(null=True)
    
class Product(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(null=False)
    remaining_amount = models.IntegerField(null=False, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    product_category = models.ManyToManyField(ProductCategory)

    def __str__(self):
        return f"{self.name}"

class Cart(models.Model):
    customer_id = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    create_date = models.DateTimeField(null=False)
    expired_in = models.IntegerField(null=False, default=60)

class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, null=False, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, default=1)



class Order(models.Model):
    customer_id = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    order_date = models.DateField(null=False)
    remark = models.TextField(null=True)

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, default=1)

class Payment(models.Model):
    order_id = models.OneToOneField(Order, null=False, on_delete=models.CASCADE)
    payment_date = models.DateField(null=False)
    remark = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

class PaymentItem(models.Model):
    payment_id = models.ForeignKey(Payment, null=False, on_delete=models.CASCADE)
    order_item_id = models.OneToOneField(OrderItem, null=False, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

class PaymentMethod(models.Model):
    payment_id = models.ForeignKey(Payment, null=False, on_delete=models.CASCADE)
    class Method(models.TextChoices):
        QR = "QR"
        CREDIT = "CREDIT"

    method = models.CharField(
        choices=Method,
        default=Method.QR,
        null=False
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    





    
    







