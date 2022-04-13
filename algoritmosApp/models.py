#from django.db import models
from djongo import models

# Create your models here.
class Departments(models.Model):
	departamentId = models.AutoField(primary_key=True)
	departamentName = models.CharField(max_length=600)

class Nodes(models.Model):
	id = models.IntegerField(null=False)
	name = models.CharField(max_length=25)
	gender = models.CharField(max_length=20)

	class Meta:
		abstract = True 

class Links(models.Model):
	source = models.IntegerField(null=False)
	target = models.IntegerField(null=False)

	class Meta:
		abstract = True

	def __str__(self):
		return str(self.source)

class Graphs(models.Model):
	grafoId = models.AutoField(primary_key=True)
	grafoName = models.CharField(max_length=50,null=True)
	nodes = models.ArrayField(
        model_container=Nodes,null = True,default=[]
    )
	links = models.ArrayField(
        model_container=Links, null = True,default=[]
    )