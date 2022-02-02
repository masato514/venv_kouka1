from django.shortcuts import render
from django.views import generic
from .forms import Kouka1Form

class Kouka1View(generic.FormView):
  template_name ="kouka1.html"
  form_class = Kouka1Form
