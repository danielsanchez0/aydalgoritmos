from django.db import models

# Create your models here.

class Departments(models.Model):
	departamentId = models.AutoField(primary_key=True)
	departamentName = models.CharField(max_length=600)