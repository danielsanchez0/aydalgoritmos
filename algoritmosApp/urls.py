#from django.conf.urls import urls
from django.urls import re_path as url
from algoritmosApp import views

urlpatterns=[
	url(r'^department$',views.departmentApi),
	url(r'^department/([0-9]+)$',views.departmentApi)
]