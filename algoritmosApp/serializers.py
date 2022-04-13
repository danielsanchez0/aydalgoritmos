from lib2to3.pytree import Node
from rest_framework import serializers
from algoritmosApp.models import Departments,Graphs

class DepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Departments
		fields = ("departamentId","departamentName")

class GrafoSerializer(serializers.ModelSerializer):
	nodes = serializers.ListField(child=serializers.DictField())
	links = serializers.ListField(child=serializers.DictField())
	class Meta:
		model = Graphs
		fields = ("grafoId","grafoName","nodes","links")