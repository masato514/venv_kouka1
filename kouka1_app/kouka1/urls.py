from django.urls import path
from . import views

app_name='kouka1'
urlpatterns =[
  path('kouka1', views.Kouka1View.as_view(), name='kouka1')
]