#from django.conf.urls import urls
from django.urls import re_path as url
from algoritmosApp import views

urlpatterns = [
    url(r'^graph$', views.graphApi),
    url(r'^graph/([0-9]+)$', views.graphApi),
    url(r'^archivo$', views.simple_upload),
    url(r'^image$', views.img_upload),
    url(r'^imagexc$', views.img_ex),
    url(r'^randomgraph$', views.random_graph),
    url(r'^xml/([0-9]+)$', views.export_xml),
]
