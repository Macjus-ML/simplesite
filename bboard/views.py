from django.shortcuts import render

from .models import Bb
from .models import Rubric

def index(request):
    bbs = Bb.objects.all()  
    rubrics = Rubric.objects.all()
    context = {'bbs':bbs, 'rubrics': rubrics}   
    return render(request,'bboard/index.html',context)
    
def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs':bbs,
               'rubrics':rubrics,
               'current_rubric':current_rubric}
    return render(request,'bboard/by_rubric.html',context)


