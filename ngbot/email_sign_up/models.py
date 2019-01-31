from django.db import models

HUMAN_SEX = [
    ("M", "Male"),
    ("F", "Female")
]
COUNTRIES = [
    ('US', 'United States'),
    ('BR', "Brazil"),
]

class Person(models.Model):

    firstname = models.TextField(max_length=1000, blank=True, null=True)
    lastname = models.TextField(max_length=1000, blank=True, null=True)
    email = models.EmailField(max_length=1000, blank=True, null=True)
    password = models.TextField(max_length=1000, blank=True, null=True)
    country = models.TextField(max_length=1000, choices=COUNTRIES, blank=True, null=True)
    sex = models.CharField(max_length=100, choices=HUMAN_SEX, blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    emailCreated = models.BooleanField(blank=True, null=True)
    ngCreated = models.BooleanField(blank=True, null=True)
    username = models.TextField(max_length=1000, blank=True, null=True)