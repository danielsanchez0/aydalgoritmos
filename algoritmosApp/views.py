from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from algoritmosApp.models import Departments,Graphs
from algoritmosApp.serializers import DepartmentSerializer, GrafoSerializer

import networkx as nx
import matplotlib.pyplot as plt

from algoritmosApp.control.graphDrawControl import grapDrawControl

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

@csrf_exempt
def graphApi(request,id=0):
	if request.method=='GET':
		if id == 0:
			graphs = Graphs.objects.all()
			grafos_serializer = GrafoSerializer(graphs,many=True)
			return JsonResponse(grafos_serializer.data,safe=False)
		elif id != 0 and id != None:
			graphs = Graphs.objects.get(grafoId=id)
			grafos_serializer = GrafoSerializer(graphs,many=False)

			#print(grafo_serializer.data.nodes)

			return JsonResponse(grafos_serializer.data,safe=False)

	elif request.method=='POST':
		grafo_data = JSONParser().parse(request)
		grafos_serializer = GrafoSerializer(data=grafo_data)
		if grafos_serializer.is_valid():
			grafos_serializer.save()
			return JsonResponse("añadido exitosamente", safe=False)
		return JsonResponse("fallo el añadido",safe=False)

	elif request.method=='PUT':
		grafo_data=JSONParser().parse(request)

		print(grafo_data)
		grafo = Graphs.objects.get(grafoId = grafo_data['grafoId'])
		
		grafo.nodes = [{
			
		}]

		grafo.save()
		#grafos_serializer = GrafoSerializer(grafo,many=False)
		#grafos_serializer.save()
		return JsonResponse("añadido exitosamente", safe=False)

		#grafos_serializer = GrafoSerializer(data=grafo_data)

		#if grafos_serializer.is_valid():
		#	grafos_serializer.save()
		#	return JsonResponse("añadido exitosamente", safe=False)
		#return JsonResponse("fallo el añadido",safe=False)
		
		#grafo_serializer = GrafoSerializer(grafo,data=grafo_data)
		#if grafo_serializer.is_valid():
		#	grafo_serializer.save()
		#	return JsonResponse("actualizado exitosamente", safe=False)
		#return JsonResponse("fallo el actualizado",safe=False)

	elif request.method=='DELETE':
		grafo = Graphs.objects.get(grafoId=id)
		grafo.delete()
		return JsonResponse("eliminado exitosamente", safe=False)