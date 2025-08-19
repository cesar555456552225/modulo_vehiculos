from django.contrib import admin
from . models import Aprendiz, Curso, InstructorCurso, AprendizCurso
# Register your models here.

admin.site.register(Aprendiz)
admin.site.register(Curso)
admin.site.register(InstructorCurso)
admin.site.register(AprendizCurso)