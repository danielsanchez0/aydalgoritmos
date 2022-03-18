from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from algoritmosApp.models import Departments
from algoritmosApp.serializers import DepartmentSerializer

# Create your views here.

@csrf_exempt
def departmentApi(request,id=0):
	if request.method=='GET':
		departments = Departments.objects.all()
		departments_serializer = DepartmentSerializer(departments,many=True)
		return JsonResponse(departments_serializer.data,safe=False)

	elif request.method=='POST':
		department_data = JSONParser().parse(request)
		departments_serializer = DepartmentSerializer(data=department_data)
		if departments_serializer.is_valid():
			departments_serializer.save()
			return JsonResponse("añadido exitosamente", safe=False)
		return JsonResponse("fallo el añadido",safe=False)

	elif request.method=='PUT':
		department_data=JSONParser().parse(request)
		department=Departments.objects.get(departmentId = department_data['departmentId'])
		departments_serializer = DepartmentSerializer(department,data=department_data)
		if departments_serializer.is_valid():
			departments_serializer.save()
			return JsonResponse("actualizado exitosamente", safe=False)
		return JsonResponse("fallo el actualizado",safe=False)

	elif request.method=='DELETE':
		department=Departments.objects.get(departmentId=id)
		department.delete()
		return JsonResponse("eliminado exitosamente", safe=False)