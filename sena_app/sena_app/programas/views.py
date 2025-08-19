from django.shortcuts import render
from django.template import loader
from .models import Programa
from django.http import HttpResponse
from .forms import ProgramaForm
from django.views.generic import FormView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
# Create your views here.

def programas(request):
    lista_programas = Programa.objects.all()
    template = loader.get_template('programas.html')
    context ={
        'programas' : lista_programas,
    }
    return HttpResponse(template.render(context, request))

def main (request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render)

class ProgramaFormView(FormView):
    template_name = 'crear_programa.html'
    form_class = ProgramaForm
    suuccess_url = '../programas/'

    def form_valid(self, form):
        programa = form.save()

        messages.success(
            self.request,
            f"El programa {programa.nombre} se ha creado."
        )
        return super().form_valid(form)