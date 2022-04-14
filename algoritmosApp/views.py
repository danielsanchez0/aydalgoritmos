from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from algoritmosApp.models import Departments,Graphs
from algoritmosApp.serializers import DepartmentSerializer, GrafoSerializer

import networkx as nx
import matplotlib.pyplot as plt


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
		grafo = Graphs.objects.get(grafoId = grafo_data['grafoId'])

		if grafo_data['tarea'] == "addNode":
			grafo.nodes.append({"id": grafo_data["id"], 
							"name": "Nodo "+str(grafo_data["id"]),
							"label": "N"+str(grafo_data["id"]),
							"data":{},
							"type":"",
							"radius":1.5,
							"coordenates":None
							})
		elif grafo_data['tarea'] == "addLinks":
			grafo.links.append({"source": grafo_data["source"],
								"target": grafo_data["target"],
								"distance": grafo_data["distance"]})

		if grafo_data['tarea'] == "removeNode":
			aux = None
			i = 0
			j = 0
			auxL = []
			while i <len(grafo.nodes) and aux is None:
				# print(grafo.nodes[i]["id"])
				if grafo.nodes[i]["id"] == grafo_data["id"]:
					aux = grafo.nodes[i]
					# print(aux)
				i= i +1
			if aux is not None:
				grafo.nodes.remove(aux)
			print("TAMAÑO ",len(grafo.links))
			while j <len(grafo.links):
				print(grafo.links[j]["target"])
				if grafo.links[j]["source"] == grafo_data["id"] or grafo.links[j]["target"] == grafo_data["id"]:
					print("entró ",grafo.links[j])
					auxL.append(grafo.links[j])
				j = j+1
			if len(auxL)>0:
				for el in auxL:
					grafo.links.remove(el)
		grafo.save()
		
		return JsonResponse("añadido exitosamente", safe=False)

	elif request.method=='DELETE':
		grafo_data=JSONParser().parse(request)
		
		if grafo_data['tarea'] == "grafo":
			grafo = Graphs.objects.get(grafoId=id)
			grafo.delete()
		return JsonResponse("eliminado exitosamente", safe=False)