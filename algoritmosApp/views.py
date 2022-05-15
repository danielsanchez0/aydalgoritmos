from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pyrsistent import T
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from algoritmosApp.models import Departments,Graphs
from algoritmosApp.serializers import DepartmentSerializer, GrafoSerializer

import networkx as nx
import matplotlib.pyplot as plt

from django.core.files.storage import FileSystemStorage
import urllib.request
import json
import random
from datetime import datetime

from algoritmosApp.Control.archivos import archivosControl

def export_xml(request, id=0):
	graphs = Graphs.objects.get(grafoId=id)
	grafos_serializer = GrafoSerializer(graphs,many=False)

	d = grafos_serializer.data
	xmlstr = archivosControl.jsonToXML(d)

	with open("./media/xml_export/json_to_xml_"+str(graphs.grafoId)+".xml", "w") as f:
		f.write(xmlstr)

	info = {
		"grafoId": graphs.grafoId,
		"link": "http://127.0.0.1:8000/media/xml_export/json_to_xml_"+str(graphs.grafoId)+".xml"
	}

	return JsonResponse(info,safe=False)

def random_graph(request):
	grafo_data=JSONParser().parse(request)
	print(grafo_data)
	cantidad_nodos = int(grafo_data['cant_nodos'])
	cantidad_aristas = int(grafo_data['cant_aristas'])

	nodos = []
	links = []
	nodos_id = []
	combinaciones = []

	for i in range(1,cantidad_nodos+1):
		nodos_id.append(i)
		nodo = {
				"id": i,
				"name": "Nodo "+str(i),
				"label": "N"+str(i),
				"data": "{}",
				"type": "",
				"radius": 12,
				"coordenates": None
			}

		nodos.append(nodo)

	for i in range(cantidad_aristas):
		combinacion = random.choices(nodos_id,k=2)

		if combinacion[0] != combinacion[1]:
	 		if combinacion not in combinaciones and [combinacion[1],combinacion[0] not in combinaciones]:
	 			combinaciones.append(combinacion)
      
	for i in combinaciones:
  		link = {
		    "source": i[0],
		    "target": i[1],
		    "distance": random.randint(1,200)
		  }

  		links.append(link)

	grafoName = "Random"+str(format(datetime.now()))

	grafo = Graphs(grafoName=grafoName,nodes=nodos,links=links)
	grafo.save()

	grafos_serializer = GrafoSerializer(grafo,many=False)
	return JsonResponse(grafos_serializer.data,safe=False)

def img_upload(request):
	myfile = request.FILES['myfile']
	print(myfile)
	fs = FileSystemStorage()
	filename = fs.save(myfile.name+".jpg", myfile)
	upload_file_url = fs.url(filename)

	link_servidor = "http://localhost:8000"
	direccion = str(link_servidor+str(upload_file_url))
	print(direccion)
	resultado = archivosControl.grafoToPDF(direccion)

	return JsonResponse(resultado, safe=False)

def img_ex(request):
	myfile = request.FILES['myfile']
	print(myfile)
	fs = FileSystemStorage()
	filename = fs.save(myfile.name+".jpg", myfile)
	upload_file_url = fs.url(filename)

	link_servidor = "http://localhost:8000"
	direccion = str(link_servidor+str(upload_file_url))
	print(direccion)
	resultado = archivosControl.graphToExcel(direccion)

	return JsonResponse(resultado, safe=False)

def simple_upload(request):
	myfile = request.FILES['myfile']
	print(myfile)
	fs = FileSystemStorage()
	filename = fs.save(myfile.name, myfile)
	upload_file_url = fs.url(filename)
	link_servidor = "http://localhost:8000"

	direccion = str(link_servidor+str(upload_file_url))
	data = None

	if archivosControl.getExtensionFile(direccion) == '.json':
		with urllib.request.urlopen(direccion) as url:
			s = url.read()
			my_json = s.decode('utf8').replace("'", '"')
			data = json.loads(my_json)
			print(type(data))

	elif archivosControl.getExtensionFile(direccion) == '.xml':
		data = archivosControl.xmlToJson(direccion)
		#data = json.dumps(s)
		print(data)

	if  data['grafoId'] != None and data['grafoName'] != None:
		grafo = Graphs(grafoName=data['grafoName'],nodes=data['nodes'],links=data['links'])
		grafo.save()

		grafos_serializer = GrafoSerializer(grafo,many=False)
		return JsonResponse(grafos_serializer.data,safe=False)

	return JsonResponse(upload_file_url,safe=False)

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
			#print("Grafo ", grafos_serializer.data)
			return JsonResponse(grafos_serializer.data,safe=False)

	elif request.method=='POST':
		grafo_data = JSONParser().parse(request)
		grafos_serializer = GrafoSerializer(data=grafo_data)
		if grafos_serializer.is_valid():
			grafos_serializer.save()

			graphs = Graphs.objects.all()
			grafo_serializer = GrafoSerializer(graphs,many=True)
			return JsonResponse(grafo_serializer.data,safe=False)
			
		return JsonResponse("fallo el añadido",safe=False)

	elif request.method=='PUT':
		print("PETICION PUT")
		grafo_data=JSONParser().parse(request)
		grafo = Graphs.objects.get(grafoId = grafo_data['grafoId'])
		#print(grafo_data)
		if grafo_data['tarea'] == "back":
			grafo.nodes = grafo_data["nodes"]
			grafo.links = grafo_data["links"]
		if grafo_data['tarea'] == "reset":
			#print("Llegó ", grafo_data)
			grafo.nodes = grafo_data["nodes"]
			grafo.links = grafo_data["links"]
		if grafo_data['tarea'] == "addNode":
			exist = False
			i = 0
			while i < len(grafo.nodes) and exist is False:
				if grafo.nodes[i]["id"] == grafo_data["id"]:
					exist = True
				i = i +1
			if exist is False:
				grafo.nodes.append({"id": grafo_data["id"], 
								"name": "Nodo "+str(grafo_data["id"]),
								"label": "N"+str(grafo_data["id"]),
								"data":{},
								"type":"",
								"radius":grafo_data["radius"],
								"coordenates":None
								})
		elif grafo_data['tarea'] == "updateNode":
			i = 0
			changed = False
			while i < len(grafo.nodes) and changed is False:
				if grafo.nodes[i]["id"] == grafo_data["id"]:
					if "name" in grafo_data:
						grafo.nodes[i]["name"] = grafo_data["name"]
						changed = True
					if "label" in grafo_data:
						grafo.nodes[i]["label"] = grafo_data["label"]
						changed = True
					if "radius" in grafo_data and grafo_data["radius"] >0:
						grafo.nodes[i]["radius"] = grafo_data["radius"]
						changed = True
					if "data" in grafo_data:
						grafo.nodes[i]["data"] = grafo_data["data"]
						changed = True
					if "type" in grafo_data:
						grafo.nodes[i]["type"] = grafo_data["type"]
						changed = True
					if "coordenates" in grafo_data:
						grafo.nodes[i]["coordenates"] = grafo_data["coordenates"]
						changed = True
				i=i+1
		elif grafo_data['tarea'] == "addLinks":
			#print("Llegó ", grafo_data)
			exist = False
			i=0 
			cont = 0
			while i< len(grafo.nodes) and cont <2: # comprobar que sea nodos existentes
				if grafo_data["source"] == grafo.nodes[i]["id"]:
					cont = cont +1
				if grafo_data["target"] == grafo.nodes[i]["id"]:
					cont = cont +1
				i = i +1
			#print("	nodos ", cont)
			if cont == 2:	# los nodos existen
				i = 0
				while i < len(grafo.links) and exist is False:
					if grafo.links[i]["source"] == grafo_data["source"] and grafo.links[i]["target"] == grafo_data["target"] :
						exist = True
					i = i +1
				if exist is False: # la arista no existe
					grafo.links.append({"source": grafo_data["source"],
										"target": grafo_data["target"],
										"distance": grafo_data["distance"]})
		
		if grafo_data['tarea'] == "updateLink":
			if "distance" in grafo_data:
				k=0
				changed = False
				while k <len(grafo.links) and changed is False:
					if grafo.links[k]["source"] == grafo_data["source"] and grafo.links[k]["target"] == grafo_data["target"]:
						#print(grafo.links[k]["source"], " / ", grafo.links[k]["target"])
						grafo.links[k]["distance"] = grafo_data["distance"]
						changed = True
					k = k +1

		if grafo_data['tarea'] == "removeLink":
			k=0
			removed = False
			aux = None
			while k <len(grafo.links) and removed is False:
				if grafo.links[k]["source"] == grafo_data["source"] or grafo.links[k]["target"] == grafo_data["target"]:
					aux = grafo.links[k]
					removed = True
				k = k+1
			if aux is not None:
				grafo.links.remove(aux)
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
			#print("TAMAÑO ",len(grafo.links))
			while j <len(grafo.links):
				print(grafo.links[j]["target"])
				if grafo.links[j]["source"] == grafo_data["id"] or grafo.links[j]["target"] == grafo_data["id"]:
					#print("entró ",grafo.links[j])
					auxL.append(grafo.links[j])
				j = j+1
			if len(auxL)>0:
				for el in auxL:
					grafo.links.remove(el)
		grafo.save()
		grafos_serializer = GrafoSerializer(grafo,many=False)
		#print("RESPUESTA ", grafos_serializer)
		return JsonResponse(grafos_serializer.data,safe=False)

	elif request.method=='DELETE':
		grafo = Graphs.objects.get(grafoId=id)
		grafo.delete()
		graphs = Graphs.objects.all()
		grafo_serializer = GrafoSerializer(graphs,many=True)
		return JsonResponse(grafo_serializer.data,safe=False)