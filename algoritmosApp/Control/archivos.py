import os
import json
from xml.dom import minidom
import urllib.request
import xml.etree.cElementTree as e

class archivosControl():
	def getExtensionFile(path):
		root, extension = os.path.splitext(path)
		return extension

	def xmlToJson(address):
		#file = minidom.parse(address)

		with urllib.request.urlopen(address) as url:
			archivo = url.read()
			codificado = archivo.decode("utf-8")
			file = minidom.parseString(codificado) 

		name = file.getElementsByTagName("grafoId")[0]
		grafoId =  int(name.firstChild.data)

		name = file.getElementsByTagName("grafoName")[0]
		grafoName = name.firstChild.data

		nodos = []
		links = []

		node = file.getElementsByTagName("node")
		for n in node:
			id = n.getElementsByTagName("id")[0]
			name = n.getElementsByTagName("name")[0]
			label = n.getElementsByTagName("label")[0]
			data = n.getElementsByTagName("data")[0]
			tipo = n.getElementsByTagName("type")[0]
			radius = n.getElementsByTagName("radius")[0]
			coordenates = n.getElementsByTagName("coordenates")[0]

			nodo = {
		      "id": int(id.childNodes[0].data),
		      "name": name.childNodes[0].data,
		      "label": label.childNodes[0].data,
		      "data": data.childNodes[0].data,
		      "type": None,
		      "radius": float(radius.childNodes[0].data),
		      "coordenates": None
			}

			nodos.append(nodo)

		link = file.getElementsByTagName("link")
		for l in link:
		  	source = l.getElementsByTagName("source")[0]
		  	target = l.getElementsByTagName("target")[0]
		  	distance = l.getElementsByTagName("distance")[0]

		  	arista = {
		      "source": int(source.childNodes[0].data),
		      "target": int(target.childNodes[0].data),
		      "distance": int(distance.childNodes[0].data)
		  	}

		  	links.append(arista)

		grafo = {
		    "grafoId": grafoId,
		    "grafoName": grafoName,
		    "nodes": nodos,
		    "links": links
		}
		
		return grafo

	def jsonToXML(d):
		r = e.Element("Graph")

		e.SubElement(r,"grafoId").text = str(d["grafoId"])                      # Edit the element's tail
		e.SubElement(r,"grafoName").text = d["grafoName"]

		nodes = e.SubElement(r,"nodes")
		links = e.SubElement(r,"links")

		for z in d["nodes"]:
		    nodo = e.SubElement(nodes,"node")
		    e.SubElement(nodo,"id").text = str(z["id"])
		    e.SubElement(nodo,"name").text = z["name"]
		    e.SubElement(nodo,"label").text = z["label"]
		    e.SubElement(nodo,"data").text = z["data"]
		    e.SubElement(nodo,"type").text = z["type"]
		    e.SubElement(nodo,"radius").text = str(z["radius"])
		    e.SubElement(nodo,"coordenates").text = str(z["coordenates"])

		for z in d["links"]:
		    link = e.SubElement(links,"link")
		    e.SubElement(link,"source").text = str(z["source"])
		    e.SubElement(link,"target").text = str(z["target"])
		    e.SubElement(link,"distance").text = str(z["distance"])

		a = e.ElementTree(r)
		xmlstr = (minidom.parseString(e.tostring(r)).toprettyxml(indent = "   "))
		return xmlstr