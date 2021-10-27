import datetime

from django.db import models


def sectionImage(instance, filename):
    return '/'.join(['Images/sectionsImages', str(instance.name), filename])


class Section(models.Model):
    name = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to=sectionImage, help_text=name, null=True)

    def __str__(self):
        return self.name


def productImage(instance, filename):
    return '/'.join(['Images/productsImages', str(instance.name), filename])


class Product(models.Model):
    statu = [
        ('new', 'new'),
        ('old', 'old'),  # recently added turn into old after 1 month
    ]

    name = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to=productImage, help_text=name, null=True)
    description = models.CharField(max_length=50, blank=True)
    price = models.FloatField(max_length=6)
    section = models.ForeignKey(Section, related_name='sections', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, choices=statu, blank=True, null=True, default='new')
    date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.name


class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    offer = models.CharField(max_length=50, blank=True)
    date = models.DateField()

    def __str__(self):
        return self.product.name


class Favourite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    pro = [
        ('in progress', 'in progress'),
        ('arrived', 'arrived'),
        ('canceled', 'canceled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    progress = models.CharField(max_length=50, choices=pro, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=11, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name


class Client(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    fav = models.ForeignKey(Favourite, on_delete=models.CASCADE, null=True)

    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)

    # password_confirm = models.CharField(max_length=20)

    def __str__(self):
        return self.username
