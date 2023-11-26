from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from .models import Task, Categories
from .serializers import CategoriesSerializer
from .serializers import TaskSerializer
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
import django_filters
from django_filters import rest_framework as filters
from rest_framework import status
#api

from .models import *
from .forms import *

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    cats = Categories.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['cats'] = self.cats
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category', None)
        if category:
            queryset = queryset.filter(category__name=category, user=self.request.user)
        else:
            queryset = queryset.filter(user=self.request.user)
        return queryset

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','category', 'filter', 'hashtag', 'description', 'complete', 'notice','priority']
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','category', 'filter','hashtag', 'description', 'complete', 'notice', 'priority']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)
    
@api_view(['GET'])
def api_root(request, format=None):
        return Response({
        'tasks': reverse('task-list', request=request, format=format),
        'categories': reverse('categories-list-create', request=request, format=format),
        'important_tasks': reverse('important-tasks-api', request=request, format=format),
    })   

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['title']

    @action(detail=False, methods=['GET'])
    def custom_action_list(self, request):
        tasks = Task.objects.filter(complete=True)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=True, methods=['POST'])
    def custom_action_detail(self, request, pk=None):
    
        task = self.get_object()
    
        return Response({"message": f"Custom action on task {task.title}"})
    
class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    @action(detail=False, methods=['GET'])
    def custom_action_list(self, request):
       
        return Response({"message": "Custom action on category list"})

    @action(detail=True, methods=['POST'])
    def custom_action_detail(self, request, pk=None):
     
        category = self.get_object()
     
        return Response({"message": f"Custom action on category {category.name}"})   
