from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from PIL import Image ###Liron added
import os

# Create your models here.

num_only = RegexValidator(r'^[0-9 ]*$', 'Only numbers allowed.')


def future(value):
    current_time = timezone.now()
    if value < current_time:
        raise ValidationError('Please provide valid Future Data')


class Treatment(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.name}"


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer_id = models.CharField(max_length=9, unique=True)
    name = models.CharField(max_length=50, blank=False, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50, null=True)
    p_number = models.CharField(max_length=20, blank=False, validators=[num_only])
    age = models.IntegerField(null=True)
    birth_date = models.DateField(null=True)
    date_joined = models.DateField(null=True)
    # image = models.ImageField(null=True,blank=True,default='/placeholder.png')

    def __str__(self):
        return f"{self.name} "


class Appointment(models.Model):
    date = models.DateTimeField(validators=[future])
    treatment = models.ForeignKey(Treatment, on_delete=models.RESTRICT)
    customer = models.ForeignKey(
        Customer, related_name="customer", null=True, on_delete=models.CASCADE)
    visit_choices = (
        ('New-Customer', 'New-Customer'),
        ('Follow-up', 'Follow-up'),
    )
    visit_type = models.CharField(
        max_length=30, choices=visit_choices, default='New-Customer')
    status_choices = (
        ('Scheduled', 'Scheduled'),
        ('Done', 'Done'),
        ('Canceled', 'Canceled')
    )
    status = models.CharField(
        max_length=20, choices=status_choices, default='Scheduled')

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"Customer: {self.customer} | treatment type: {self.treatment} |  appointment date: {self.date}"


class Appointment_History(models.Model):
    appointment = models.ForeignKey(
        Appointment, null=True, related_name="appointment", on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, null=True, related_name="customer_history", on_delete=models.CASCADE)


class Bday_benefit(models.Model):
    bday_customer = models.ForeignKey(
        Customer, null=True, related_name="bday_customer", on_delete=models.CASCADE)
    benefits = models.CharField(max_length=50)

# ###Liron added
# class Image(models.Model):
#     title=models.CharField(max_length=100)
#     image=models.ImageField(upload_to='Posted_Images') ##I changed it to imagefield instead of file field on the 19.02.2023 21:48

#     def __str__(self):
#         return self.title

#     class Meta:
#         db_table = 'Product Images'
# ###Liron added

# ##chat gpt suggested replaceing the image model to: (adding the upload_to)
# def upload_to(instance, filename):
#     return 'Posted_Images/{}'.format(filename)


def upload_to(instance, filename):
    folder_name = 'Posted_Images'
    directory = os.path.join('media', folder_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(folder_name, filename)

class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to=upload_to)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Product Images'



class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ###Liron added
    image = models.ForeignKey(Image, on_delete=models.SET_NULL,null=True)
    ###Liron added

    def __str__(self):
        return f"{self.name} "


# ##Liron added after watching Eyal's pillow session:
# class APIs(models.Model):
#     title=models.CharField(max_length=100)
#     content=models.TextField()
#     image=models.ImageField(upload_to='Posted_Images')


#     def __str__(self):
#         return self.title
