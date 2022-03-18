from rest_framework import serializers
from algoritmosApp.models import Departments

class DepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Departments
		fields = ("departamentId","departamentName")