from rest_framework import serializers
from algoritmosApp.models import Departments,Graphs

class DepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Departments
		fields = ("departamentId","departamentName")

class GrafoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Graphs
		fields = ("grafoId","nodos","aristas")