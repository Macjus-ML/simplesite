from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView
from django.core.paginator import Paginator
from django.forms import modelformset_factory

from .models import Bb, Rubric
from .forms import  BbForm

def index(request):
    rubrics = Rubric.objects.all()
    bbs = Bb.objects.all()
    paginator = Paginator(bbs,2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)  
    context = {'rubrics': rubrics, 'page': page, 'bbs': page.object_list}   
    return render(request,'bboard/index.html',context)
    
def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs':bbs,
               'rubrics':rubrics,
               'current_rubric':current_rubric}
    return render(request,'bboard/by_rubric.html',context)

    

def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric',
                    kwargs={'rubric_id':bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request,'bboard/create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request,'bboard/create.html', context)

def delete(request, pk):
    bb = Bb.objects.get(pk=pk)
    if request.method == 'POST':
        bb.delete()
        return HttpResponseRedirect(reverse('bboard:by_rubric',
                kwargs={'rubric_id': bb.rubric.pk}))
    else:
        context = {'bb':bb}
        return render(request, 'bboard/bb_confirm_delete.html',context)

def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric,fields=('name',),
                        can_order=True, can_delete=True)

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    rubric = form.save(commit=False)
                    rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    rubric.save()
                return redirect('bboard:index')
    else:
        formset =RubricFormSet()
    context = {'formset' :formset}
    return render(request, 'bboard/rubrics.html', context)
    

class BbCreateView(CreateView):
    template_name='bboard/create.html'
    form_class=BbForm
    success_url= reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics']=Rubric.objects.all()
        return context

class BbIndexView(TemplateView):
    template_name = 'bboard.index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["bbs"] = Bb.objects.all() 
        context['rubrics']=Rubric.objects.all()
        return context
    
class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubric'] = Rubric.objects.all() 
        return context

class BbByRubricView(ListView):
    template_name='bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["rubric"] = Rubric.objects.all()
        context["current_rubric"] = Rubric.objects.get(
                                            pk=self.kwargs['rubric_id']) 
        return context

class BbAddView(FormView):
    template_name= 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["rubrics"] = Rubric.objects.all() 
        return context
    
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        self.objects = super().get_form(form_class)
        return self.objects
    
    def get_success_url(self):
        return reverse('bboard:by_rubric', 
            kwargs = {'rubric_id':self.objects.cleaned_data['rubric'].pk})

class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["rubrics"] = Rubric.objects.all()
        return context

class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["rubrics"] = Rubric.objects.all()
        return context
    
class BbIndexArchView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["rubrics"] = Rubric.objects.all()
        return context   
    
   
    

    

