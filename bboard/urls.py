from django.urls import path
from .views import index, by_rubric
from .views import BbCreateView,BbDetailView
from .views import add_and_save

urlpatterns = [
    path('add/', BbCreateView.as_view(),name= 'add'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('add/', add_and_save, name='add'), 
    path('<int:rubric_id>/',by_rubric, name='by_rubric'),
    path('',index, name='index'),
]

