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

    def json_model(self):
        json_model = {}
        json_model['firstname'] = self.firstname
        json_model['lastname'] = self.lastname
        json_model['email'] = self.email
        json_model['password'] = self.password
        json_model['country'] = self.country
        json_model['sex'] = self.sex
        json_model['day'] = self.day
        json_model['month'] = self.month
        json_model['year'] = self.year
        json_model['emailCreated'] = self.emailCreated
        json_model['ngCreated'] = self.ngCreated
        json_model['username'] = self.username
        return json_model
