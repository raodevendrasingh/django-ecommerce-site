from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=200, null=False)
    password = models.CharField(max_length=128, default='123456')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    tags = models.ManyToManyField(Tag)
    size = models.CharField(max_length=20, null=True)
    color = models.CharField(max_length=20, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default='item')
    description = models.CharField(
        max_length=500, default='', blank=True, null=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='WishlistItem')

    def __str__(self):
        return self.customer.name + "'s Wishlist"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True

        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # @property
    # def get_total(self):
    #     total = self.product.price * self.quantity
    #     return total
    @property
    def get_total(self):
        if self.product and hasattr(self.product, 'price'):
            total = self.product.price * self.quantity
            return total
        else:
            # Handle the case where self.product is None or does not have a 'price' attribute
            raise ValueError("Invalid product or product price not available.")

    def __str__(self):
        return self.product


class ShippingDetails(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    address_level_1 = models.CharField(max_length=50, null=False)
    address_level_2 = models.CharField(max_length=50, null=False)
    country = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    pincode = models.CharField(max_length=50, null=False)
    contact = PhoneNumberField()

    def __str__(self):
        return self.address_level_1

    class Meta:
        verbose_name = "Shipping Details"
        verbose_name_plural = "Shipping Details"  # Set the plural form explicitly
