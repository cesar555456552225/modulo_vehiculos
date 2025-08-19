from django.shortcuts import render
from django.template import loader
from .models import Instructor
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .forms import InstructorForm
from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
# Create your views here.

def instructores(request):
    lista_instructores = Instructor.objects.all()
    template = loader.get_template('instructor.html')
    context={
        'instructores' : lista_instructores,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def detalle_instructor(request, instructor_id):
    instructor=get_object_or_404(Instructor, id=instructor_id)
    #cursos_coordinados = instructor.cursos_coordinador.all()
    #cursos_impartidos = instructor.cursos_impartidos.all()
    template = loader.get_template('detalle_instructor.html')
    context = {
        'instructor' : instructor,
        #'cursos_coordinados': cursos_coordinados,
        #'cursos_impartidos': cursos_impartidos,
    }
    return HttpResponse(template.render(context, request))

class InstructorFormView(FormView):
    template_name = 'crear_instructor.html'
    form_class = InstructorForm
    success_url = '../instructores/'

    def form_valid(self, form):
        instructor = form.save()

        messages.success(
            self.request,
            f'El instructor {instructor.nombre} {instructor.apellido} ha sido creado exitosamente.'
        )
        return super().form_valid(form)
    